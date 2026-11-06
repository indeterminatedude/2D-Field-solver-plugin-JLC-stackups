import { useEffect, useRef } from "react";
import { createFileRoute } from "@tanstack/react-router";
import { previewPathPrefix } from "@/lib/preview-path-prefix";

export const Route = createFileRoute("/")({ component: Home });

function solverUrl() {
  if (typeof window === "undefined") return "/solver.html";
  const prefix = previewPathPrefix(window.location.hostname, window.location.pathname);
  return prefix ? `${prefix}/solver.html` : "/solver.html";
}

function Home() {
  const root = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const mount = root.current;
    if (!mount || mount.dataset.ready === "1") return;
    let cancelled = false;

    fetch(solverUrl())
      .then((res) => {
        if (!res.ok) throw new Error(`solver ${res.status}`);
        return res.text();
      })
      .then((html) => {
        if (cancelled || !mount) return;
        const doc = new DOMParser().parseFromString(html, "text/html");
        document.getElementById("solver-style")?.remove();
        const style = document.createElement("style");
        style.id = "solver-style";
        style.textContent = [...doc.querySelectorAll("style")]
          .map((node) => node.textContent ?? "")
          .join("\n");
        document.head.appendChild(style);

        const scripts = [...doc.querySelectorAll("script")].map((node) => node.textContent ?? "");
        doc.querySelectorAll("script").forEach((node) => node.remove());
        mount.innerHTML = doc.body.innerHTML;
        mount.dataset.ready = "1";

        for (const code of scripts) {
          const el = document.createElement("script");
          el.textContent = code;
          document.body.appendChild(el);
        }
      })
      .catch((err) => {
        if (!mount) return;
        mount.textContent = `Could not load the field solver (${String(err)}).`;
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return <div id="solver-root" ref={root} style={{ minHeight: "100dvh" }} />;
}
