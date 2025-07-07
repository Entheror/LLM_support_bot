import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://web_backend:8000', 
        changeOrigin: true,
        rewrite: (path) => {
          const newPath = path.replace(/^\/api/, '');
          console.log(`[Proxy] Rewriting ${path} to ${newPath}`);
          return newPath;
        },
        secure: false,
        ws: false,
        logLevel: 'debug',
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log(`[Proxy] Sending request to http://web_backend:8000${req.url}`);
            proxyReq.setHeader('Host', 'web_backend:8000');
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log(`[Proxy] Response from ${req.url}: ${proxyRes.statusCode}`);
            console.log(`[Proxy] Response headers: ${JSON.stringify(proxyRes.headers)}`);
            console.log(`[Proxy] Response body: ${proxyRes.body ? proxyRes.body.toString() : 'No body'}`);
          });
          proxy.on('error', (err, req, res) => {
            console.log(`[Proxy] Error for ${req.url}: ${err.message}`);
            res.writeHead(500, { 'Content-Type': 'text/plain' });
            res.end(`Proxy error: ${err.message}`);
          });
        },
        buffer: false,
        timeout: 10000,
        proxyTimeout: 10000,
        agent: false
      },
      '/llm': {
        target: 'http://llm_service:8000', 
        changeOrigin: true,
        rewrite: (path) => {
          const newPath = path.replace(/^\/llm/, '');
          console.log(`[Proxy] Rewriting ${path} to ${newPath}`);
          return newPath;
        },
        secure: false,
        ws: false,
        logLevel: 'debug',
        configure: (proxy) => {
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log(`[Proxy] Sending request to http://llm_service:8000${req.url}`);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log(`[Proxy] Response from ${req.url}: ${proxyRes.statusCode}`);
            console.log(`[Proxy] Response headers: ${JSON.stringify(proxyRes.headers)}`);
          });
          proxy.on('error', (err, req, res) => {
            console.log(`[Proxy] Error for ${req.url}: ${err.message}`);
            res.writeHead(500, { 'Content-Type': 'text/plain' });
            res.end(`Proxy error: ${err.message}`);
          });
        },
        buffer: false,
        timeout: 10000,
        proxyTimeout: 10000,
        agent: false
      }
    }
  }
})