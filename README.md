# Meteo archiv (tmep.cz → GitHub Actions → GitHub Pages)

Tento repozitář pravidelně stahuje data z [tmep.cz](https://tmep.cz) a ukládá je do `data/history.csv`.
Stránka v `docs/index.html` je vykresluje (teplota °C, vlhkost %).

## Nastavení

1. V repozitáři otevři **Settings → Secrets and variables → Actions** a přidej:
   - `TMEP_ID` = `4065`
   - `TMEP_KEY` = `hgzwodurps` *(doporučeno vygenerovat vlastní export key a tenhle jen považovat za demo)*

2. Zapni **GitHub Pages**:
   - Settings → Pages → Source: *Deploy from a branch*
   - Branch: `main` / Folder: `/docs`

3. Akce běží každých 15 minut (cron je v UTC). Můžeš spustit ručně v **Actions → Pull Tmep.cz data → Run workflow**.

4. Data najdeš v `data/history.csv`, historie v Gitu slouží jako audit log.

## Úprava intervalu
V `.github/workflows/pull_tmep.yml` uprav cron, např. každých 10 minut:
