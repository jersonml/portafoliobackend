from django.db import models

import random
from string import ascii_lowercase

class SlugNameManager(models.Manager):

    CODE_LENGTH = 10

    def create(self, **kwargs):

        pool = ascii_lowercase
        name = kwargs.get('name') + '-'
        category_or_id = kwargs.get('category','id')
        slug_name = kwargs.get('slug_name',''.join(category_or_id))
        while self.filter(slug_name=slug_name).exists():
            slug_name = ''.join(f'{name}{random.choices(pool,k=self.CODE_LENGTH)}')
        kwargs['slug_name'] = slug_name
        return super(SlugNameManager, self).create(**kwargs)