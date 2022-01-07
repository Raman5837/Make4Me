from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category
from StoreRoom.models import Product
# Register your models here.


class CategoryAdmin(admin.TabularInline):
    model = Category
    prepopulated_fields = {'slug': ('categoryName',)}
    list_display = ('categoryName',)
    list_filter = ['categoryName']
    search_fields = ['categoryName']

class CategoryAdminMPTT(DraggableMPTTAdmin):
    mptt_indent_field = "categoryName"
    list_display = ('tree_actions', 'indented_title',
                    'related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('categoryName',)}
    inlines = [CategoryAdmin]
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related Products (For This Specific Category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related Products (In Tree)'


admin.site.register(Category, CategoryAdminMPTT)