from django.contrib import admin
from .models import Product, ProductVariants, ReviewAndRating, ProductGallery, Slider, ProductCustomization

import admin_thumbnails

# Register your models here.

    
class ProductVariantsInline(admin.TabularInline):
    model = ProductVariants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True
    
    
class ProductVariantsAdmin(admin.ModelAdmin):
    list_display = ['product','variationCategory','variationValue','isActive','image_tag',]
    list_editable = ['isActive',]
    list_filter = ['product', 'variationCategory', 'variationValue','isActive',]
    
@admin_thumbnails.thumbnail('productImage')    
class ProductGalleryInLine(admin.TabularInline):
    model = ProductGallery
    extra = 0
    list_display = ['product', 'image_tag']
    list_filter = ['product']
    search_fields = ['product']


@admin_thumbnails.thumbnail('productImage')
class ProductAdmin(admin.ModelAdmin):
    
    list_display = ['productName', 'category', 'inStock', 'isAvailable', 'image_tag']
    list_filter = ['productName', 'category']
    search_fields = ['productName', 'category']
    inlines = [ProductGalleryInLine,ProductVariantsInline]
    prepopulated_fields = {'slug': ('productName',)}

class ReviewAndRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'subject', 'createdAt']
    list_filter = ['product', 'subject', 'createdAt', 'modifiedAt']
    search_fields = ['product']
    
@admin_thumbnails.thumbnail('productImage')
class ProductGalleryAdmin(admin.ModelAdmin):
    
    list_display = ['product', 'image_tag']
    list_filter = ['product']
    search_fields = ['product']
    
@admin_thumbnails.thumbnail('sliderImage')     
class SliderAdmin(admin.ModelAdmin):
    list_display = ['punchLine_1', 'punchLine_2', 'url', 'isActive', 'image_tag']
    search_fields = ['isActive']

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariants, ProductVariantsAdmin)
admin.site.register(ReviewAndRating, ReviewAndRatingAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)
admin.site.register(Slider, SliderAdmin)
admin.site.register(ProductCustomization)
