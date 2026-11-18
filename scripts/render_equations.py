"""
보고서 수식(LaTeX)을 고해상도 PNG로 렌더링 (matplotlib mathtext 사용, LaTeX 설치 불필요)

실행
    python scripts/render_equations.py
출력
    presentation_charts/equations/eq1_car.png, eq2_welch_t.png (DPI 300, 흰 배경)
    presentation_charts/equations/*_transparent.png (투명 배경, 슬라이드용)
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT_DIR = Path(__file__).resolve().parent.parent / "presentation_charts" / "equations"

EQUATIONS = {
    # 3절 방법론: 누적초과수익률(복리 누적 후 전체 표본 평균 차감)
    "eq1_car": r"$\mathrm{CAR}[0,k] = \prod_{t=0}^{k}\,(1 + R_t) - 1 - \overline{\mathrm{CAR}[0,k]}$",
    # 3절 방법론: Welch t 통계량
    "eq2_welch_t": r"$t = \dfrac{\bar{R}_{\mathrm{event}} - \bar{R}_{\mathrm{control}}}"
                   r"{\sqrt{s_{\mathrm{event}}^{2}/n_{\mathrm{event}} + s_{\mathrm{control}}^{2}/n_{\mathrm{control}}}}$",
}


def render(name: str, tex: str, transparent: bool) -> Path:
    plt.rcParams["mathtext.fontset"] = "cm"
    fig = plt.figure(figsize=(0.01, 0.01))
    fig.text(0, 0, tex, fontsize=28, color="black")
    suffix = "_transparent" if transparent else ""
    path = OUT_DIR / f"{name}{suffix}.png"
    fig.savefig(path, dpi=300, bbox_inches="tight", pad_inches=0.15,
                transparent=transparent, facecolor="none" if transparent else "white")
    plt.close(fig)
    return path


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, tex in EQUATIONS.items():
        for tr in (False, True):
            print(render(name, tex, tr))


if __name__ == "__main__":
    main()
