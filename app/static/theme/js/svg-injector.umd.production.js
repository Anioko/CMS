! function(t, e) {
    "object" == typeof exports && "undefined" != typeof module ? e(exports) : "function" == typeof define && define.amd ? define(["exports"], e) : e((t = t || self).SVGInjector = {})
}(this, function(t) {
    "use strict";
    var e, r = function(t) {
            return t.cloneNode(!0)
        },
        n = function() {
            return "file:" === window.location.protocol
        },
        i = new Map,
        o = {},
        a = function(t, e) {
            o[t] = o[t] || [], o[t].push(e)
        },
        l = function(t) {
            for (var e = function(e, n) {
                    setTimeout(function() {
                        if (Array.isArray(o[t])) {
                            var n = i.get(t),
                                a = o[t][e];
                            (n instanceof SVGSVGElement || n instanceof HTMLElement) && a(null, r(n)), n instanceof Error && a(n), e === o[t].length - 1 && delete o[t]
                        }
                    }, 0)
                }, n = 0, a = o[t].length; n < a; n++) e(n)
        },
        s = 0,
        c = [],
        u = {},
        f = "http://www.w3.org/1999/xlink",
        d = function(t, e, o, d, p) {
            var v = t.getAttribute("data-src") || t.getAttribute("src");
            if (v && /\.svg/i.test(v)) {
                if (-1 !== c.indexOf(t)) return c.splice(c.indexOf(t), 1), void(t = null);
                c.push(t), t.setAttribute("src", ""),
                    function(t, e) {
                        if (i.has(t)) {
                            var o = i.get(t);
                            return o instanceof SVGSVGElement || o instanceof HTMLElement ? void e(null, r(o)) : o instanceof Error ? void e(o) : void a(t, e)
                        }
                        i.set(t, void 0), a(t, e);
                        var s = new XMLHttpRequest;
                        s.onreadystatechange = function() {
                            try {
                                if (4 === s.readyState) {
                                    if (404 === s.status || null === s.responseXML) throw new Error(n() ? "Note: SVG injection ajax calls do not work locally without adjusting security setting in your browser. Or consider using a local webserver." : "Unable to load SVG file: " + t);
                                    if (!(200 === s.status || n() && 0 === s.status)) throw new Error("There was a problem injecting the SVG: " + s.status + " " + s.statusText);
                                    s.responseXML instanceof Document && s.responseXML.documentElement && i.set(t, s.responseXML.documentElement), l(t)
                                }
                            } catch (e) {
                                i.set(t, e), l(t)
                            }
                        }, s.open("GET", t), s.overrideMimeType && s.overrideMimeType("text/xml"), s.send()
                    }(v, function(r, n) {
                        if (!n) return c.splice(c.indexOf(t), 1), t = null, void p(r);
                        var i = t.getAttribute("id");
                        i && n.setAttribute("id", i);
                        var a = t.getAttribute("title");
                        a && n.setAttribute("title", a);
                        var l = t.getAttribute("width");
                        l && n.setAttribute("width", l);
                        var h = t.getAttribute("height");
                        h && n.setAttribute("height", h);
                        var g = Array.from(new Set((n.getAttribute("class") || "").split(" ").concat(["injected-svg"], (t.getAttribute("class") || "").split(" ")))).join(" ").trim();
                        n.setAttribute("class", g);
                        var A = t.getAttribute("style");
                        A && n.setAttribute("style", A), n.setAttribute("data-src", v);
                        var m = [].filter.call(t.attributes, function(t) {
                            return /^data-\w[\w-]*$/.test(t.name)
                        });
                        if (Array.prototype.forEach.call(m, function(t) {
                                t.name && t.value && n.setAttribute(t.name, t.value)
                            }), o) {
                            var b, w, y, E, S = {
                                clipPath: ["clip-path"],
                                "color-profile": ["color-profile"],
                                cursor: ["cursor"],
                                filter: ["filter"],
                                linearGradient: ["fill", "stroke"],
                                marker: ["marker", "marker-start", "marker-mid", "marker-end"],
                                mask: ["mask"],
                                path: [],
                                pattern: ["fill", "stroke"],
                                radialGradient: ["fill", "stroke"]
                            };
                            Object.keys(S).forEach(function(t) {
                                w = S[t];
                                for (var e = function(t, e) {
                                        var r;
                                        E = (y = b[t].id) + "-" + ++s, Array.prototype.forEach.call(w, function(t) {
                                            for (var e = 0, i = (r = n.querySelectorAll("[" + t + '*="' + y + '"]')).length; e < i; e++) {
                                                var o = r[e].getAttribute(t);
                                                o && !o.match(new RegExp("url\\(#" + y + "\\)")) || r[e].setAttribute(t, "url(#" + E + ")")
                                            }
                                        });
                                        for (var i = n.querySelectorAll("[*|href]"), o = [], a = 0, l = i.length; a < l; a++) {
                                            var c = i[a].getAttributeNS(f, "href");
                                            c && c.toString() === "#" + b[t].id && o.push(i[a])
                                        }
                                        for (var u = 0, d = o.length; u < d; u++) o[u].setAttributeNS(f, "href", "#" + E);
                                        b[t].id = E
                                    }, r = 0, i = (b = n.querySelectorAll(t + "[id]")).length; r < i; r++) e(r)
                            })
                        }
                        n.removeAttribute("xmlns:a");
                        for (var x, j, k = n.querySelectorAll("script"), G = [], M = 0, T = k.length; M < T; M++)(j = k[M].getAttribute("type")) && "application/ecmascript" !== j && "application/javascript" !== j && "text/javascript" !== j || ((x = k[M].innerText || k[M].textContent) && G.push(x), n.removeChild(k[M]));
                        if (G.length > 0 && ("always" === e || "once" === e && !u[v])) {
                            for (var V = 0, N = G.length; V < N; V++) new Function(G[V])(window);
                            u[v] = !0
                        }
                        var O = n.querySelectorAll("style");
                        Array.prototype.forEach.call(O, function(t) {
                            t.textContent += ""
                        }), n.setAttribute("xmlns", "http://www.w3.org/2000/svg"), n.setAttribute("xmlns:xlink", f), d(n), t.parentNode && t.parentNode.replaceChild(n, t), c.splice(c.indexOf(t), 1), t = null, p(null, n)
                    })
            } else p(new Error("Attempted to inject a file with a non-svg extension: " + v))
        };
    (e = t.EvalScripts || (t.EvalScripts = {})).Always = "always", e.Once = "once", e.Never = "never";
    t.SVGInjector = function(e, r) {
        var n = void 0 === r ? {} : r,
            i = n.afterAll,
            o = void 0 === i ? function() {} : i,
            a = n.afterEach,
            l = void 0 === a ? function() {} : a,
            s = n.beforeEach,
            c = void 0 === s ? function() {} : s,
            u = n.evalScripts,
            f = void 0 === u ? t.EvalScripts.Never : u,
            p = n.renumerateIRIElements,
            v = void 0 === p || p;
        if (e && "length" in e)
            for (var h = 0, g = 0, A = e.length; g < A; g++) d(e[g], f, v, c, function(t, r) {
                l(t, r), e && "length" in e && e.length === ++h && o(h)
            });
        else e ? d(e, f, v, c, function(t, r) {
            l(t, r), o(1), e = null
        }) : o(0)
    }, Object.defineProperty(t, "__esModule", {
        value: !0
    })
});
//# sourceMappingURL=svg-injector.umd.production.js.map