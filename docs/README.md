# Pikapika Documentation Site

This directory contains the static website for Pikapika that is deployed to GitHub Pages.

## 🌐 Live Site

The documentation is automatically deployed to GitHub Pages at:
- **https://[your-username].github.io/pikapika/**

Replace `[your-username]` with your GitHub username.

## 📁 Structure

- `index.html` - Main documentation page
- `styles.css` - Styling with modern dark theme and animations
- `script.js` - Interactive features and animations

## 🚀 Deployment

The site is automatically deployed using GitHub Actions whenever changes are pushed to the `main` or `master` branch.

### Workflow File
`.github/workflows/deploy-pages.yml`

### How It Works
1. Push changes to the `main` or `master` branch
2. GitHub Actions automatically builds and deploys the `docs` folder
3. The site is published to GitHub Pages

## ⚙️ GitHub Pages Setup

To enable GitHub Pages for your repository:

1. Go to your repository on GitHub
2. Click on **Settings**
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select:
   - Source: **GitHub Actions**
5. Save the settings

The workflow will automatically deploy your site on the next push.

## 🎨 Customization

Feel free to customize the documentation:

- **Colors**: Edit CSS variables in `styles.css` under `:root`
- **Content**: Modify `index.html` to update features, examples, etc.
- **Animations**: Adjust or add animations in `script.js`

## 🔧 Local Development

To preview the site locally:

1. Open `index.html` in your browser, or
2. Use a local server:
   ```bash
   # Python 3
   python -m http.server 8000
   
   # Node.js (if you have http-server installed)
   npx http-server
   ```
3. Navigate to `http://localhost:8000`

## 📝 License

Same as the main project - MIT License
