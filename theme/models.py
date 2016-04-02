
from django.db import models
from django.utils.translation import ugettext_lazy as _

from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import RichText, Orderable, Slugged
from mezzanine.pages.models import Page
from mezzanine.utils.models import upload_to


class HomePage(Page, RichText):
    '''
    A page representing the format of the home page
    '''
    heading = models.CharField(max_length=200,
        help_text="The heading under the gallery")
    subheading = models.CharField(max_length=200,
        help_text="The subheading just below the heading")
    featured_works_heading = models.CharField(max_length=200,
        default="Featured Works")
    featured_portfolio = models.ForeignKey("Portfolio", blank=True, null=True,
        help_text="If selected items from this portfolio will be featured "
                  "on the home page.")
    content_heading = models.CharField(max_length=200,
        default="About us!")
    latest_posts_heading = models.CharField(max_length=200,
        default="Latest Posts")

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class Slide(Orderable):
    '''
    A slide in a slider connected to a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="slides")
    image = FileField(verbose_name=_("Image"),
        upload_to=upload_to("theme.Slide.image", "slider"),
        format="Image", max_length=255, null=True, blank=True)


class IconBlurb(Orderable):
    '''
    An icon box on a HomePage
    '''
    homepage = models.ForeignKey(HomePage, related_name="blurbs")
    icon = models.CharField(max_length=100,
        help_text="A font awesome icon name. i.e. icon-compass.  More here: "
                  "http://fortawesome.github.io/Font-Awesome/icons/")
    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.CharField(max_length=2000, blank=True,
        help_text="Optional, if provided clicking the blurb will go here.")


COLUMNS_CHOICES = (
    ('6', 'Two columns'),
    ('4', 'Three columns'),
    ('3', 'Four Columns'),
)


class Portfolio(Page):
    '''
    A collection of individual portfolio items
    '''
    optional_content = RichTextField(blank=True)
    columns = models.CharField(max_length=1, choices=COLUMNS_CHOICES,
        default='3')
    class Meta:
        verbose_name = _("Portfolio")
        verbose_name_plural = _("Portfolios")


class PortfolioItem(Page, RichText):
    '''
    An individual portfolio item, should be nested under a Portfolio
    '''
    featured_image = FileField(verbose_name=_("Featured Image"),
        upload_to=upload_to("nuro_proj.PortfolioItem.featured_image", "portfolio"),
        format="Image", max_length=255, null=True, blank=True)
    short_description = RichTextField(blank=True)
    categories = models.ManyToManyField("PortfolioItemCategory",
                                        verbose_name=_("Categories"),
                                        blank=True,
                                        related_name="portfolioitems")
    href = models.CharField(max_length=2000, blank=True,
        help_text="A link to the finished project (optional)")

    class Meta:
        verbose_name = _("Portfolio item")
        verbose_name_plural = _("Portfolio items")


class PortfolioItemImage(Orderable):
    '''
    An image for a PortfolioItem
    '''
    portfolioitem = models.ForeignKey(PortfolioItem, related_name="images")
    file = FileField(_("File"), max_length=200, format="Image",
        upload_to=upload_to("vital_theme.PortfolioItemImage.file", "portfolio"))

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")


class PortfolioItemCategory(Slugged):
    """
    A category for grouping portfolio items into a series.
    """

    class Meta:
        verbose_name = _("Portfolio Item Category")
        verbose_name_plural = _("Portfolio Item Categories")
        ordering = ("title",)
