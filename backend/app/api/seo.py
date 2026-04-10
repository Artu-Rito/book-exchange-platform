from fastapi import APIRouter, Response, Request
from datetime import datetime

router = APIRouter(tags=["SEO"])


@router.get("/sitemap.xml")
async def get_sitemap(request: Request):
    """
    Генерация sitemap.xml для SEO
    """
    base_url = str(request.base_url).rstrip('/')
    today = datetime.now().strftime('%Y-%m-%d')
    
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{base_url}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>{base_url}/books</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>{base_url}/statistics</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.7</priority>
  </url>
</urlset>'''
    
    return Response(content=sitemap, media_type="application/xml")


@router.get("/robots.txt")
async def get_robots(request: Request):
    """
    Возвращает robots.txt для SEO
    """
    base_url = str(request.base_url).rstrip('/')
    
    robots = f'''User-agent: *
Allow: /
Allow: /books
Allow: /statistics

# Disallow private routes
Disallow: /profile/
Disallow: /reservations/
Disallow: /calendar/
Disallow: /api/

# Sitemap
Sitemap: {base_url}/sitemap.xml
'''
    
    return Response(content=robots, media_type="text/plain")
