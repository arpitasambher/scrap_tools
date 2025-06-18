from crewai_tools.tools.selenium_scraping_tool.selenium_scraping_tool import SeleniumScrapingTool

tool = SeleniumScrapingTool(
    website_url='https://www.instagram.com/arruu.u77/',
    css_element='article img',
#     📸 Image thumbnails	article img
# 🔗 Post links	article a
# 📝 Post captions	div._a9zs (inside modal after clicking post)
# ❤️ Like counts (in post)	section span._aamw
    wait_time=10,
    return_html=True
)

result = tool.run()
with open("insta", "w", encoding="utf-8") as f:
    f.write(result)

print("✅ Scraped content saved to scraped_output.txt")