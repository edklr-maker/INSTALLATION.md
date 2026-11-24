/* Met chaque croquis du storyboard dans une planche A3 paysage avec cartouche.
   Exécuté par exporter_croquis.py après le code des planches (NS, mk, P). */
const COUDEE_M = 0.525;
const VERSION = "v1 · 24/11/2026";
/* k = nombre de coudées par unité de dessin ; null = sans échelle */
const ECHELLES = {
  "00": {cm: true},
  "09": null, "16": null, "A": null,
  "13": {k: 50, note: "échelle horizontale ; profondeurs exagérées"},
  "14": {k: 1000}, "15": {k: 100}
};
const CSS = `
:root{--paper:#ffffff;--sheet:#ffffff;--ink:#1b2833;--line:#34506a;--muted:#5b6c79;--fill:#c3d2dc;--soft:#e4ecf1;--soft2:#d3e0e9;
--cote:#b0392b;--hyp:#8c6a12;--water:#9cc3dc;--rule:#cdd8df;
--f-disp:"Barlow Condensed","Bahnschrift SemiCondensed","Bahnschrift","Arial Narrow",sans-serif;
--f-body:"Source Serif 4",Georgia,serif;--f-mono:"IBM Plex Mono",Consolas,ui-monospace,monospace}
.dr *{vector-effect:non-scaling-stroke}
.wall{fill:var(--fill);stroke:var(--line);stroke-width:1.4}
.wallh{fill:none;stroke:var(--hyp);stroke-width:1.2;stroke-dasharray:6 4}
.soft{fill:var(--soft);stroke:var(--line);stroke-width:.8}
.soft2{fill:var(--soft2);stroke:var(--line);stroke-width:.8}
.bg{fill:var(--sheet);stroke:var(--line);stroke-width:1}
.ln{fill:none;stroke:var(--line);stroke-width:1.4}
.thin{fill:none;stroke:var(--line);stroke-width:.8}
.dash{fill:none;stroke:var(--line);stroke-width:1;stroke-dasharray:7 5}
.hyp{fill:none;stroke:var(--hyp);stroke-width:1.4;stroke-dasharray:6 4}
.bar{fill:var(--cote);stroke:none;opacity:.55}
.water{fill:var(--water);stroke:var(--line);stroke-width:1}
.dim{stroke:var(--cote);stroke-width:1;fill:none}
.ext{stroke:var(--cote);stroke-width:.6;fill:none;opacity:.7}
.tx{fill:var(--ink);font-family:var(--f-mono)}
.lbl{fill:var(--ink);font-family:var(--f-disp);font-weight:600;letter-spacing:.02em}
.mut{fill:var(--muted);font-family:var(--f-mono)}
.tc{fill:var(--cote);font-family:var(--f-mono);font-weight:500}
.th{fill:var(--hyp);font-family:var(--f-mono)}
.solid{fill:var(--line);stroke:none}
.frame{fill:none;stroke:var(--ink);stroke-width:2.2}
.frame2{fill:none;stroke:var(--ink);stroke-width:.8}
.cell{fill:none;stroke:var(--ink);stroke-width:.8}
.k-num{font-family:var(--f-mono);font-size:15px;fill:var(--cote);letter-spacing:2px}
.k-title{font-family:var(--f-disp);font-weight:600;font-size:46px;fill:var(--ink)}
.k-ref{font-family:var(--f-mono);font-size:15px;fill:var(--muted)}
.k-lab{font-family:var(--f-mono);font-size:12px;fill:var(--muted);letter-spacing:1.5px}
.k-txt{font-family:var(--f-mono);font-size:15px;fill:var(--ink)}
.k-small{font-family:var(--f-mono);font-size:13px;fill:var(--ink)}
.sb-a{fill:var(--ink)} .sb-b{fill:#fff;stroke:var(--ink);stroke-width:1}
`;
function E(n, a, parent, text) {
  const e = document.createElementNS(NS, n);
  for (const k in a) e.setAttribute(k, a[k]);
  if (text !== undefined) e.textContent = text;
  if (parent) parent.appendChild(e);
  return e;
}
function joli(v) {
  const c = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500, 5000, 10000, 20000];
  let best = c[0];
  for (const x of c) if (x <= v) best = x;
  return best;
}
function fmt(n) { return n.toLocaleString("fr-FR", {maximumFractionDigits: 2}); }
function planche(p) {
  const W = 1600, H = 1131;
  const s = E("svg", {xmlns: NS, viewBox: `0 0 ${W} ${H}`, width: "420mm", height: "297mm"});
  E("style", {}, s, CSS);
  E("rect", {x: 0, y: 0, width: W, height: H, fill: "#ffffff"}, s);
  E("rect", {x: 20, y: 20, width: W - 40, height: H - 40, class: "frame"}, s);
  const AX = 50, AY = 45, AW = 1500, AH = 830;
  const vb = p.vb.split(/\s+/).map(Number);
  const d = mk(p.vb, p.fs, p.draw, p.t);
  d.setAttribute("x", AX); d.setAttribute("y", AY); d.setAttribute("width", AW); d.setAttribute("height", AH);
  d.setAttribute("preserveAspectRatio", "xMidYMid meet"); d.setAttribute("class", "dr");
  s.appendChild(d);
  const px = Math.min(AW / vb[2], AH / vb[3]); /* pixels de planche par unité de dessin */

  /* cartouche */
  const CY = 900, CH = H - 20 - CY;
  E("line", {x1: 20, y1: CY, x2: W - 20, y2: CY, class: "frame"}, s);
  const c1 = 20, c2 = 800, c3 = 1190, c4 = W - 20;
  [c2, c3].forEach(x => E("line", {x1: x, y1: CY, x2: x, y2: H - 20, class: "cell"}, s));

  E("text", {x: c1 + 24, y: CY + 34, class: "k-num"}, s, `PLANCHE ${p.n} · TEMPLE D'ÉZÉCHIEL`);
  E("text", {x: c1 + 24, y: CY + 92, class: "k-title"}, s, p.t);
  E("text", {x: c1 + 24, y: CY + 130, class: "k-ref"}, s, `Ézéchiel ${p.r}`);
  E("text", {x: c1 + 24, y: CY + 175, class: "k-lab"}, s, `CROQUIS POUR MODÉLISATION BLENDER · ${VERSION}`);

  /* échelle */
  E("text", {x: c2 + 22, y: CY + 30, class: "k-lab"}, s, "ÉCHELLE");
  const info = Object.prototype.hasOwnProperty.call(ECHELLES, p.n) ? ECHELLES[p.n] : {k: 1};
  const bx = c2 + 22, by = CY + 70;
  if (info === null) {
    E("text", {x: bx, y: by + 6, class: "k-txt"}, s, "Schéma sans échelle");
  } else {
    let pxU, unit, L, conv;
    if (info.cm) { pxU = px; unit = "cm"; L = joli(300 / pxU); conv = `${fmt(L / 52.5)} coudée`; }
    else { pxU = px / info.k; unit = "coudées"; L = joli(300 / pxU); conv = `≈ ${fmt(L * COUDEE_M)} m`; }
    const len = L * pxU, n = 5;
    for (let i = 0; i < n; i++) E("rect", {x: bx + i * len / n, y: by, width: len / n, height: 10, class: i % 2 ? "sb-b" : "sb-a"}, s);
    E("rect", {x: bx, y: by, width: len, height: 10, fill: "none", stroke: "#1b2833", "stroke-width": 1}, s);
    E("text", {x: bx, y: by - 8, class: "k-small"}, s, "0");
    E("text", {x: bx + len, y: by - 8, class: "k-small", "text-anchor": "end"}, s, `${fmt(L)} ${unit}`);
    E("text", {x: bx, y: by + 32, class: "k-small"}, s, `${fmt(L)} ${unit} ${conv}`);
    if (!info.cm) {
      const mmParCoudee = pxU * 420 / W;
      const ratio = COUDEE_M * 1000 / mmParCoudee;
      const r = ratio > 1000 ? Math.round(ratio / 100) * 100 : ratio > 100 ? Math.round(ratio / 10) * 10 : Math.round(ratio);
      E("text", {x: bx, y: by + 54, class: "k-small"}, s, `imprimé en A3 : ≈ 1:${r.toLocaleString("fr-FR")}`);
    }
    if (info.note) E("text", {x: bx, y: by + 76, class: "k-small", fill: "#8c6a12"}, s, info.note);
  }
  E("text", {x: c2 + 22, y: CY + 166, class: "k-small"}, s, "1 coudée longue = 52,5 cm");
  E("text", {x: c2 + 22, y: CY + 186, class: "k-small"}, s, "1 roseau = 6 coudées = 3,15 m");

  /* légende */
  E("text", {x: c3 + 22, y: CY + 30, class: "k-lab"}, s, "LÉGENDE");
  const lg = [
    ["wall", "maçonnerie cotée par le texte"],
    ["wallh", "hypothèse ou déduction"],
    ["soft", "sol, cour, terrain"],
    ["dim", "cote en coudées longues"]
  ];
  lg.forEach(([cl, txt], i) => {
    const y = CY + 52 + i * 30;
    if (cl === "dim") E("line", {x1: c3 + 22, y1: y + 8, x2: c3 + 58, y2: y + 8, class: "dim", "stroke-width": 2}, s);
    else E("rect", {x: c3 + 22, y: y, width: 36, height: 16, class: cl}, s);
    E("text", {x: c3 + 70, y: y + 13, class: "k-small"}, s, txt);
  });
  E("text", {x: c3 + 22, y: CY + 185, class: "k-small", fill: "#5b6c79"}, s, "Plans : nord en haut, est à droite (sauf mention)");
  return s;
}
const out = document.getElementById("out");
P.forEach(p => {
  const div = document.createElement("div");
  div.setAttribute("data-n", p.n);
  div.setAttribute("data-t", p.t);
  div.setAttribute("data-svg", encodeURIComponent(new XMLSerializer().serializeToString(planche(p))));
  out.appendChild(div);
});
