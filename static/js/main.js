// static/js/main.js
// Single-file client logic for product listing (AJAX refresh, edit modal, delete, states).
// Includes toast dedupe and defensive initialization.

(function () {
    // ---------------------------
    // Prevent double-initialization
    // ---------------------------
    if (window.__MAIN_JS_LOADED__) {
        // already loaded -> do nothing
        return;
    }
    window.__MAIN_JS_LOADED__ = true;

    // ---------------------------
    // Toast dedupe wrapper
    // ---------------------------
    (function installToastDedupe() {
        if (!window.showToast) {
        // fallback if base didn't define it
        window.showToast = function (msg, type) {
            console.log("[toast]", type || "info", msg);
        };
        return;
        }
        if (window.__showToastWrapped__) return;
        window.__showToastWrapped__ = true;

        const orig = window.showToast;
        const seen = new Map();
        const TTL = 1000; // 1 second dedupe window

        window.showToast = function (msg, type = "success") {
        try {
            const key = (type || "") + "|" + (msg || "");
            const now = Date.now();
            const last = seen.get(key) || 0;
            if (now - last < TTL) {
            // drop duplicate
            return;
            }
            seen.set(key, now);
        } catch (e) {
            console.error("toast-dedupe error", e);
        }
        return orig(msg, type);
        };
    })();

    // ---------------------------
    // Utilities
    // ---------------------------
    function getCookie(name) {
        let v = null;
        if (!document.cookie) return null;
        document.cookie.split(";").forEach(function (c) {
        const cookie = c.trim();
        if (cookie.startsWith(name + "=")) v = decodeURIComponent(cookie.substring(name.length + 1));
        });
        return v;
    }

    function show(el) { if (el) el.classList.remove("hidden"); }
    function hide(el) { if (el) el.classList.add("hidden"); }
    function addClass(el, cls) { if (el) el && el.classList.add(...cls.split(" ")); }
    function removeClass(el, cls) { if (el) el && el.classList.remove(...cls.split(" ")); }

    const csrftoken = getCookie("csrftoken");

    // Ensure showToast exists (should be from base.html). Already wrapped above fallback.
    if (typeof window.showToast !== "function") {
        window.showToast = function (msg, type) { console.log("Toast", type, msg); };
    }

    // ---------------------------
    // Elements & config
    // ---------------------------
    const container = document.getElementById("product-list-container");
    const loadingEl = document.getElementById("product-loading");
    const emptyEl = document.getElementById("product-empty");
    const errorEl = document.getElementById("product-error");
    const refreshBtn = document.getElementById("refresh-products-btn");

    const AJAX_PRODUCT_LIST_URL = (window.APP_URLS && window.APP_URLS.ajax_product_list) || "/ajax/product_list/";

    // ---------------------------
    // fetchProductList: core refresh
    // showToastOnSuccess -> boolean (manual action shows toast)
    // ---------------------------
    async function fetchProductList(showToastOnSuccess = false) {
        if (!container) return;

        hide(errorEl);
        hide(emptyEl);

        // Fade-in loader (assumes loader has opacity-0 + transition classes)
        if (loadingEl) {
        removeClass(loadingEl, "hidden");
        requestAnimationFrame(() => removeClass(loadingEl, "opacity-0"));
        }

        if (refreshBtn) refreshBtn.disabled = true;

        try {
        const qs = window.location.search || "";
        const resp = await fetch(AJAX_PRODUCT_LIST_URL + qs, {
            headers: { "X-Requested-With": "XMLHttpRequest" },
            credentials: "same-origin",
        });

        if (!resp.ok) throw new Error("Network response was not ok: " + resp.status);

        const html = await resp.text();

        // Inject HTML fragment (server returned rendered cards)
        container.innerHTML = html;

        // Evaluate empty state from fragment
        const grid = container.querySelector("#product-grid");
        const cards = grid ? grid.children.length : 0;
        if (!cards) {
            hide(container);
            show(emptyEl);
        } else {
            show(container);
            hide(emptyEl);
        }

        if (showToastOnSuccess) {
            showToast("Products refreshed!", "success");
        }

        // Reattach direct listeners for new elements
        attachDirectDeleteListeners();
        // edit uses delegated handler below, no rebind necessary
        } catch (err) {
        console.error("Failed to fetch product list", err);
        show(errorEl);
        showToast("Failed to load products", "error");
        } finally {
        if (refreshBtn) refreshBtn.disabled = false;
        if (loadingEl) {
            addClass(loadingEl, "opacity-0");
            setTimeout(() => hide(loadingEl), 300);
        }
        }
    }

    // expose globally
    window.fetchProductList = fetchProductList;

    // ---------------------------
    // Safe Refresh button wiring (attach exactly one handler)
    // ---------------------------
    if (refreshBtn) {
        // remove previously attached handler (if any)
        if (refreshBtn._productRefreshHandler) {
        refreshBtn.removeEventListener("click", refreshBtn._productRefreshHandler);
        }

        refreshBtn._productRefreshHandler = function (e) {
        e.preventDefault();
        fetchProductList(true);
        };

        refreshBtn.addEventListener("click", refreshBtn._productRefreshHandler);
    }

    // ---------------------------
    // Edit modal handler (delegated)
    // Buttons must include data-edit-url attribute in template
    // ---------------------------
    (function attachEditHandler() {
        // Only attach once
        if (document.__editHandlerAttached__) return;
        document.__editHandlerAttached__ = true;

        document.addEventListener("click", async function (e) {
        const btn = e.target.closest(".edit-btn");
        if (!btn) return;
        e.preventDefault();

        const url = btn.dataset.editUrl || btn.getAttribute("data-edit-url");
        if (!url) {
            console.warn("edit-btn missing data-edit-url");
            return;
        }

        try {
            const resp = await fetch(url, {
            headers: { "X-Requested-With": "XMLHttpRequest" },
            credentials: "same-origin",
            });
            if (!resp.ok) throw new Error("Failed to load edit form: " + resp.status);
            const html = await resp.text();

            const formModalBody = document.getElementById("form-modal-body");
            const formModalTitle = document.getElementById("form-modal-title");
            if (!formModalBody || !formModalTitle) {
            console.warn("Modal elements missing");
            return;
            }

            formModalBody.innerHTML = html;
            formModalTitle.textContent = "Edit Product";
            if (typeof showModal === "function") showModal("form-modal");
            document.body.style.overflow = "hidden";

            const form = formModalBody.querySelector("form");
            if (form) {
            // handle submission once per load
            form.addEventListener("submit", async function (ev) {
                ev.preventDefault();
                const fd = new FormData(form);
                try {
                const save = await fetch(form.action, {
                    method: form.method || "POST",
                    headers: { "X-CSRFToken": csrftoken, "X-Requested-With": "XMLHttpRequest" },
                    credentials: "same-origin",
                    body: fd,
                });

                const data = await save.json();
                if (data.status === "success") {
                    showToast("Product updated successfully!", "success");
                    if (typeof hideModal === "function") hideModal("form-modal");
                    document.body.style.overflow = "";
                    if (typeof fetchProductList === "function") fetchProductList();
                } else {
                    // If server returned form HTML (validation error), show it
                    if (typeof data === "string" && data.includes("<form")) {
                    formModalBody.innerHTML = data;
                    }
                    showToast("Failed to update product", "error");
                }
                } catch (err) {
                console.error("Error saving product", err);
                showToast("Error saving product", "error");
                }
            }, { once: true });
            }
        } catch (err) {
            console.error(err);
            showToast("Could not load edit form", "error");
        }
        });
    })();

    // ---------------------------
    // Delete handling
    // Buttons should have data-delete-url attribute
    // ---------------------------
    async function handleDeleteButton(btn) {
        if (!btn) return;
        const url = btn.dataset.deleteUrl || btn.getAttribute("data-delete-url");
        if (!url) {
        console.warn("delete-btn missing data-delete-url");
        return;
        }

        if (!confirm("Are you sure you want to delete this product? This cannot be undone.")) return;

        try {
        const resp = await fetch(url, {
            method: "POST",
            headers: { "X-CSRFToken": csrftoken, "X-Requested-With": "XMLHttpRequest" },
            credentials: "same-origin",
        });

        if (!resp.ok) {
            const text = await resp.text().catch(() => null);
            console.error("Delete failed", resp.status, text);
            showToast("Failed to delete product", "error");
            return;
        }

        const data = await resp.json().catch(() => ({ status: "success" }));
        if (data.status === "success") {
            showToast(data.message || "Product deleted successfully!", "success");
            const card = btn.closest("article");
            if (card) card.remove();
            if (typeof fetchProductList === "function") fetchProductList();
        } else {
            showToast(data.message || "Failed to delete product", "error");
        }
        } catch (err) {
        console.error("Error deleting product", err);
        showToast("Error deleting product", "error");
        }
    }

    // delegated delete listener (attach once)
    if (!document.__deleteHandlerAttached__) {
        document.__deleteHandlerAttached__ = true;
        document.addEventListener("click", function (e) {
        const btn = e.target.closest(".delete-btn");
        if (!btn) return;
        e.preventDefault();
        handleDeleteButton(btn);
        });
    }

    // direct-attach helper (for newly injected fragments)
    function attachDirectDeleteListeners() {
        document.querySelectorAll(".delete-btn").forEach(btn => {
        if (btn.__deleteBound) return;
        btn.__deleteBound = true;
        btn.addEventListener("click", function (e) {
            e.preventDefault();
            handleDeleteButton(btn);
        });
        });
    }

    // initial attachment & initial empty sync
    document.addEventListener("DOMContentLoaded", function () {
        attachDirectDeleteListeners();

        // If page initially had no products and server rendered empty block,
        // ensure container visibility matches.
        try {
        const grid = container && container.querySelector("#product-grid");
        if (grid && grid.children.length === 0) {
            hide(container);
            show(emptyEl);
        }
        } catch (e) {
        // ignore
        }
    });

    // Expose helper for other modules
    window.attachDirectDeleteListeners = attachDirectDeleteListeners;

})();
