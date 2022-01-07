from django.db import models
from django.db.models import Avg, Count
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import  Image
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse
from Category.models import Category
from Accounts.models import Account
from django.http.response import HttpResponse
# Create your models here.

class Product(models.Model):
    
    LABEL_CHOICES = (
        ('Sale', 'Sale'),
        ('New', 'New'),
        ('Promotion', 'Promotion'),
        ('Make4Me Special', 'Make4Me Special'),
    )
    
    productName = models.CharField(max_length = 50, unique = True, verbose_name = 'Product Name')
    category = models.ForeignKey(Category, on_delete = models.CASCADE, verbose_name = 'Category')
    slug = models.SlugField(max_length = 50, unique = True, verbose_name = 'Slug')
    description = models.CharField(max_length = 100, verbose_name = 'Description')
    details = RichTextUploadingField(verbose_name = 'Product Details')
    keywords = models.TextField(blank = True, null = True, verbose_name = 'Keywords')
    label = models.CharField(choices = LABEL_CHOICES, max_length = 20, verbose_name = 'Label')
    inStock = models.PositiveIntegerField(verbose_name = 'In Stock')
    isAvailable = models.BooleanField(default = True)
    isCustomizable = models.BooleanField(default = False, verbose_name = 'Is Customizable')
    highPrice = models.FloatField(verbose_name = 'High Price')
    discountedPrice = models.FloatField(blank = True, verbose_name = 'Selling Price')
    tax = models.PositiveSmallIntegerField(default = 0, verbose_name = 'Tax')
    shippingCharge = models.FloatField(default = 0, verbose_name = 'Shipping Charge')
    productImage = models.ImageField(upload_to = 'Images/ProductImages/')
    create_at = models.DateTimeField(auto_now_add = True, editable = False, verbose_name = 'Created At')
    modified_at = models.DateTimeField(auto_now = True, editable = False, verbose_name = 'Updated At')
    
    soldCount = models.PositiveIntegerField(default = 0, verbose_name = 'Sold Count')
    
    def __str__(self):
        return self.productName
    
    def save(self, *args, **kwargs):
	    super().save(*args, **kwargs)

	    img = Image.open(self.productImage.path)
	    if img.height > 1600 or img.width > 1600:
	    	output_size = (1600, 1600)
	    	img.thumbnail(output_size)
	    	img.save(self.productImage.path)
    
    def image_tag(self):
        try:
            if self.productImage.url is not None:
                return format_html('<img src="{}" height="50" width="50" object-fit: contain/>'.format(self.productImage.url))
            else:
                return ""
        except Exception as e:
            return HttpResponse(e)
        
    def getUrl(self):
        return reverse('productDetail', args = [self.category.slug, self.slug])
    
    def averageRating(self):
        reviews = ReviewAndRating.objects.filter(product = self, status = True).aggregate(average = Avg('rating'))
        return float(reviews['average']) if reviews['average'] is not None else 0
    
    
    def countReview(self):
        reviews = ReviewAndRating.objects.filter(product = self, status = True).aggregate(count = Count('id'))
        return int(reviews['count']) if reviews['count'] is not None else 0

        
    

class VariationManager(models.Manager):
    
    def colors(self):
        return super(VariationManager, self).filter(variationCategory = 'Color', isActive = True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variationCategory = 'Size', isActive = True)
    

    
class ProductVariants(models.Model):
    
    variantChoices = (
        ('Color', 'Color'),
        ('Size', 'Size'),
    )
    
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    variationCategory = models.CharField(max_length = 50, choices = variantChoices, verbose_name = 'Type Of Variation')
    isActive = models.BooleanField(default = True, verbose_name = 'Is Active')
    create_at = models.DateTimeField(auto_now_add = True, editable = False, verbose_name = 'Created At')
    variationValue = models.CharField(max_length = 100, verbose_name = 'Enter Size Or Color')
    productImage = models.ImageField(blank = True, upload_to = 'Images/ProductImages/')

    highPrice = models.FloatField(verbose_name = 'High Price')
    discountedPrice = models.FloatField(blank = True, verbose_name = 'Selling Price')
    keywords = models.TextField(blank = True, null = True, verbose_name = 'Keywords')
    
    
    objects = VariationManager()
            
    def save(self, *args, **kwargs):
	    super().save(*args, **kwargs)

	    img = Image.open(self.productImage.path)
	    if img.height > 1600 or img.width > 1600:
	    	output_size = (1600, 1600)
	    	img.thumbnail(output_size)
	    	img.save(self.productImage.path)
    
    
    def image_tag(self):
        try:
            if self.productImage.url is not None:
                return format_html('<img src="{}" height="50" width="50" object-fit: contain/>'.format(self.productImage.url))
            else:
                return ""
        except Exception as e:
            return HttpResponse(e)
    
    
    def __str__(self):
        return f'{self.variationValue}'
            
    
    class Meta:
        verbose_name = 'Product Variant'
        verbose_name_plural = 'Product Variants'
        
class ReviewAndRating(models.Model):
    
    user = models.ForeignKey(Account, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    
    subject = models.CharField(max_length = 100, blank = True, verbose_name = 'Subject')
    review = models.TextField(max_length = 500, blank = True, verbose_name = 'Review')
    rating = models.FloatField(verbose_name = 'Rating Star',)
    ip = models.CharField(max_length = 20, blank = True, verbose_name = 'IP Address Of User')
    status = models.BooleanField(default = True, verbose_name = 'Status')
    createdAt = models.DateTimeField(auto_now_add = True, editable = False, verbose_name = 'Created At')
    modifiedAt = models.DateTimeField(auto_now = True, editable = False, verbose_name = 'Updated At')
            
            
    def __str__(self):
        return f'{self.subject} --> {self.product}'
    
    class Meta:
        verbose_name = 'Review And Rating'
        verbose_name_plural = 'Reviews And Ratings'
        
        
class ProductGallery(models.Model):
    
    product = models.ForeignKey(Product, on_delete = models.CASCADE, default = None)
    productImage = models.ImageField(upload_to = 'Images/ProductImages/', max_length = 255, verbose_name = 'Product Image')
    
    class Meta:
        verbose_name = 'Product Image Gallery'
        verbose_name_plural = 'Product Image Gallery'
        
    def save(self, *args, **kwargs):
	    super().save(*args, **kwargs)

	    img = Image.open(self.productImage.path)
	    if img.height > 1600 or img.width > 1600:
	    	output_size = (1600, 1600)
	    	img.thumbnail(output_size)
	    	img.save(self.productImage.path)
    
    def image_tag(self):
        try:
            if self.productImage.url is not None:
                return format_html('<img src="{}" height="70" width="70" object-fit: contain/>'.format(self.productImage.url))
            else:
                return ""
        except Exception as e:
            return HttpResponse(e)
    
    def __str__(self):
        return f'{self.product.productName}'
    
    
class Slider(models.Model):
    
    sliderImage = models.ImageField(upload_to = 'Images/SliderImages/', verbose_name = 'Slider Image', help_text="Size: 900 X 1920")
    punchLine_1 = models.CharField(max_length = 100, verbose_name = 'PunchLine 1')
    punchLine_2 = models.CharField(max_length = 100, blank = True, verbose_name = 'PunchLine 2')
    pickUpLine = models.CharField(max_length = 100, blank = True, verbose_name = 'Pick Up Line')
    startingAt = models.CharField(max_length = 100, blank = True, verbose_name = 'Starting From')
    
    url = models.URLField(max_length = 200, null = True, verbose_name = 'URL')
    isActive = models.BooleanField(default = True)
    
    def save(self, *args, **kwargs):
	    super().save(*args, **kwargs)

	    img = Image.open(self.sliderImage.path)
	    if img.height > 900 or img.width > 1920:
	    	output_size = (900, 1920)
	    	img.thumbnail(output_size)
	    	img.save(self.sliderImage.path)
    
    
    def image_tag(self):
        try:
            if self.sliderImage.url is not None:
                return format_html('<img src="{}" height="100" width="200" object-fit: contain/>'.format(self.sliderImage.url))
            else:
                return ""
        except Exception as e:
            return HttpResponse(e)
        
    def __str__(self):
        return f'{self.punchLine_1} {self.punchLine_2}'
    
    
class ProductCustomization(models.Model):
    
    user = models.ForeignKey(Account, on_delete = models.CASCADE, null = True)
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True)
    customizationImage = models.ImageField(upload_to = 'Images/CustomizationImages/', verbose_name = 'Customization Image')

    cutomizationNotes = models.TextField(max_length = 300, blank = True, verbose_name = 'Cutomization Notes')
    