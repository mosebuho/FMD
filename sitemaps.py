from django.contrib.sitemaps import Sitemap
from board.models import News, Column, Community


class NewsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        results = News.objects.order_by("-id")
        return results

    def location(self, obj):
        return f"/news/%s" % obj.pk

    def lastmod(self, obj):
        return obj.date


class ColumnSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1

    def items(self):
        results = Column.objects.order_by("-id")
        return results

    def location(self, obj):
        return f"/column/%s" % obj.pk

    def lastmod(self, obj):
        return obj.date


class CommunitySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        results = Community.objects.order_by("-id")
        return results

    def location(self, obj):
        return f"/community/%s" % obj.pk

    def lastmod(self, obj):
        return obj.date
