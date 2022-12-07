from django.contrib.sitemaps import Sitemap
from .models import Post
# We have defined a custom sitemap by inheriting the Sitemap class of the sitemaps module. The
# changefreq and priority attributes indicate the change frequency of your post pages and their relevance
# in your website (the maximum value is 1).



class PostSiteMap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9


    def items(self):
        return Post.published.all()

    def lastmod(self,obj):
        return obj.updated
