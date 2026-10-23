# Andrzej Baranski, Personal Academic Website

Source code for the personal website of Andrzej Baranski, Associate Professor of Economics at New York University Abu Dhabi.

**Live site:** https://www.abarmad.com

Built with [Astro](https://astro.build) and deployed to GitHub Pages with GitHub Actions.

## Tech stack

- **Astro**, a static site generator that ships almost no JavaScript
- **TypeScript** for the data files
- **Plain CSS**, with colors and fonts defined as variables in `src/styles/global.css`
- **Fontsource** for self-hosted fonts (Inter and Source Serif 4)
- **GitHub Actions + GitHub Pages** for hosting

## Project structure

```
.
├── .github/workflows/deploy.yml   # Build and deploy on every push to main
├── public/                        # Served as-is at the site root
│   ├── CNAME                      # Custom domain
│   ├── cv.pdf                     # CV shown on the CV page
│   ├── images/                    # Photo and logos
│   ├── papers/                    # PDFs of published papers
│   ├── working-papers/            # PDFs of working papers
│   ├── syllabi/                   # Course syllabi
│   └── data/                      # Replication data files
├── src/
│   ├── components/                # Header, Footer, PublicationList, CourseList
│   ├── data/                      # Editable content (see below)
│   │   ├── site.ts                # Name, roles, nav, affiliation logo
│   │   ├── news.ts                # "Recent Highlights" on the home page
│   │   ├── publications.ts        # Published, working, and in-progress papers
│   │   └── courses.ts             # Current and previous teaching
│   ├── layouts/Layout.astro       # Shared page layout and <head>
│   ├── pages/                     # Each file becomes a URL
│   │   ├── index.astro            # Home
│   │   ├── research.astro
│   │   ├── teaching.astro
│   │   └── cv.astro
│   └── styles/global.css          # Colors, fonts, base styles
├── astro.config.mjs
└── package.json
```

## License and ownership

Site content (text, publications, images, CV) © Andrzej Baranski. All rights reserved.
