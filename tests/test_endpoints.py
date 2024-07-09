from django.test import TestCase
from main_app import models


class CategoryTestCase(TestCase):
    def setUp(self):
        self.first_category: models.Category = models.Category.objects.create(
            name='Kill',
            description='Kill long description',
            statistic_counter=321,
            statistic_info='Kill Drons',
            statistic_additional_info='Kill FPV drones',
            slug='first-category',
        )
        self.second_category: models.Category = models.Category.objects.create(
            name='Humanitarian',
            en_name='Not to kill',
            description='long description',
            en_description='long description but in Eng',
            statistic_counter=123,
            statistic_info='Drons',
            statistic_additional_info='FPV drones',
            en_statistic_info='Drones EN',
            en_statistic_additional_info='FPV Drones EN',
            slug='second-category',
        )

    def test_get_all_categories(self):
        response = self.client.get('/categories/')
        assert response.status_code == 200
        sort_key = lambda x: x['id']
        assert sorted(response.json(), key=sort_key) == sorted(
            [
                {
                    'id': 1,
                    'name': 'Kill',
                    'description': 'Kill long description',
                    'statistic_counter': 321,
                    'statistic_info': 'Kill Drons',
                    'statistic_additional_info': 'Kill FPV drones',
                    'picture': None,
                },
                {
                    'id': 2,
                    'name': 'Humanitarian',
                    'description': 'long description',
                    'statistic_counter': 123,
                    'statistic_info': 'Drons',
                    'statistic_additional_info': 'FPV drones',
                    'picture': None,
                },
            ],
            key=sort_key,
        )

    def test_get_all_categories_in_en(self):
        response = self.client.get('/categories/', {'language': 'en'})
        assert response.status_code == 200
        assert response.json() == [
            {
                'id': 2,
                'name': 'Not to kill',
                'description': 'long description but in Eng',
                'statistic_counter': 123,
                'statistic_info': 'Drones EN',
                'statistic_additional_info': 'FPV Drones EN',
                'picture': None,
            }
        ]

    def get_single_category(self):
        response = self.client.get(f'/categories/{self.first_category.slug}/')
        assert response.status_code == 200
        assert response.json() == {
            'id': self.first_category.id,
            'name': self.first_category.name,
            'description': self.first_category.description,
            'statistic_counter': self.first_category.statistic_counter,
            'statistic_info': self.first_category.statistic_info,
            'statistic_additional_info': self.first_category.statistic_additional_info,
            'picture': None,
        }


class AccountsTestCase(TestCase):
    def setUp(self):
        self.account_1 = models.Account.objects.create(title='Mono', iban='1234')
        self.account_2 = models.Account.objects.create(
            title='Mono bank', description='Banka: https://foo.com'
        )

    def test_get_all_accounts(self):
        response = self.client.get('/accounts')
        assert response.status_code == 200, response
        assert response.json() == [
            {
                'id': self.account_1.id,
                'title': 'Mono',
                'iban': '1234',
                'description': None,
            },
            {
                'id': self.account_2.id,
                'title': 'Mono bank',
                'iban': None,
                'description': 'Banka: https://foo.com',
            },
        ]


class ProjectsTestCase(TestCase):
    def setUp(self):
        self.account = models.Account.objects.create(title='Mono', iban='1234')
        self.category = models.Category.objects.create(
            name='Humanitarian', en_name='Not to kill', slug='first-project-category'
        )
        self.category_2 = models.Category.objects.create(
            name='For kill', slug='second-project-category'
        )
        self.category_3 = models.Category.objects.create(
            name='For children of Donbass', slug='third-project-category'
        )
        self.project = models.Project.objects.create(
            category=self.category,
            title='UA title',
            description='UA description',
            goal=10000000,
            accumulated_current=1,
            slug='first-project',
        )
        self.project.save()
        self.project.accounts.add(self.account)
        self.project_en = models.Project.objects.create(
            category=self.category,
            title='UA title',
            description='UA description',
            en_title='EN title',
            en_description='EN description',
            goal=10000000,
            accumulated_current=1,
            slug='second-project',
        )
        self.project_en.save()
        self.project_en.accounts.add(self.account)

        self.project_diff_category = models.Project.objects.create(
            category=self.category_2,
            title='UA title 2',
            description='UA description 2',
            goal=10000000,
            accumulated_current=1,
            slug='third-project',
        )
        self.project_diff_category.save()
        self.project_diff_category.accounts.add(self.account)

        self.project_diff_category_and_language = models.Project.objects.create(
            category=self.category_3,
            title='UA title 2',
            description='UA description 2',
            en_title='EN title 2',
            en_description='EN description 2',
            goal=10000000,
            accumulated_current=1,
            slug='fourth-project',
        )
        self.project_diff_category_and_language.save()
        self.project_diff_category_and_language.accounts.add(self.account)

    def test_get_projects(self):
        response = self.client.get('/projects/')
        assert response.status_code == 200
        assert len(response.json()) == 4

    def test_get_en_projects(self):
        response = self.client.get('/projects/', {'language': 'en'})
        assert response.status_code == 200
        assert len(response.json()) == 2
        assert response.json()[0]['id'] == self.project_en.id

    def test_get_projects_by_category(self):
        response = self.client.get('/projects/', {'category_id': self.category_2.id})
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['id'] == self.project_diff_category.id

    def test_get_projects_by_category_and_language(self):
        response = self.client.get(
            '/projects/',
            {'category_id': self.category_3.id, 'language': 'en'},
        )
        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]['id'] == self.project_diff_category_and_language.id

    def test_do_not_return_finished_projects(self):
        first_response = self.client.get('/projects/')
        self.finished_project = models.Project.objects.create(
            category=self.category,
            title='Finished project',
            description='Finished project',
            goal=10000000,
            accumulated_current=10000000,
            is_finished=True,
        )
        self.finished_project.save()
        self.finished_project.accounts.add(self.account)
        second_response = self.client.get('/projects/')
        assert len(first_response.json()) == len(second_response.json())

    def test_get_single_project(self):
        response = self.client.get(f'/projects/{self.project_en.slug}/')
        expected = {
            'id': self.project_en.id,
            'title': 'UA title',
            'description': 'UA description',
            'goal': 10000000,
            'accumulated_current': 1,
            'accounts': [
                {
                    'id': self.account.id,
                    'title': 'Mono',
                    'iban': '1234',
                    'description': None,
                }
            ],
            'category': {
                'id': self.category.id,
                'name': self.category.name,
                'statistic_additional_info': self.category.statistic_additional_info,
                'statistic_info': self.category.statistic_info,
                'description': self.category.description,
                'statistic_counter': self.category.statistic_counter,
                'picture': None,
            },
            'images': [],
        }
        assert response.json() == expected, response.json()

    def test_get_related_projects(self):
        response = self.client.get(f'/projects/{self.project.id}/related_projects/')
        assert response.status_code == 200, response.status_code
        result = response.json()
        assert len(result) == 1, response.json()
        assert result[0]['id'] == self.project_en.id, result


class FoundersTestCase(TestCase):
    def setUp(self):
        self.founder_1 = models.Founder.objects.create(
            name='Foo',
            description='bar',
        )
        self.founder_2 = models.Founder.objects.create(
            name='Foo Second UA',
            description='bar Second UA',
            en_name='Foo EN',
            en_description='Bar EN',
        )

    def test_get_all_founders(self):
        response = self.client.get('/founders')
        assert response.status_code == 200, response.json()
        assert response.json() == [
            {
                'id': self.founder_1.id,
                'name': self.founder_1.name,
                'description': self.founder_1.description,
                'picture': None,
            },
            {
                'id': self.founder_2.id,
                'name': self.founder_2.name,
                'description': self.founder_2.description,
                'picture': None,
            },
        ], response.json()

    def test_get_all_founders_in_english(self):
        response = self.client.get('/founders', {'language': 'en'})
        assert response.status_code == 200, response.json()
        assert response.json() == [
            {
                'id': self.founder_1.id,
                'name': self.founder_1.en_name,
                'description': self.founder_1.en_description,
                'picture': None,
            },
            {
                'id': self.founder_2.id,
                'name': self.founder_2.en_name,
                'description': self.founder_2.en_description,
                'picture': None,
            },
        ], response.json()


class NewsTestCase(TestCase):
    """Test logic related to news endpoints."""

    def setUp(self) -> None:
        self.news_1 = models.News.objects.create(
            title='Foo UA',
            description='description UA',
            slug='first',
        )
        self.news_with_en = models.News.objects.create(
            title='Bar UA',
            description='description bar UA',
            en_title='Bar EN',
            en_description='description bar EN',
            slug='second',
        )
        self.news_with_en_2 = models.News.objects.create(
            title='Baz UA',
            description='description baz UA',
            en_title='Baz EN',
            en_description='description baz EN',
            slug='third',
        )

    def get_news(self):
        response = self.client.get('/news/')
        assert response.status_code == 200
        assert len(response.json()['results']) == 3

    def test_get_news_in_english(self):
        response = self.client.get('/news/', {'language': 'en'})
        assert response.status_code == 200
        assert len(response.json()['results']) == 2

    def test_get_single_news(self):
        response = self.client.get(f'/news/{self.news_with_en.slug}/')
        assert response.status_code == 200
        assert response.json() == {
            'id': self.news_with_en.id,
            'title': self.news_with_en.title,
            'description': self.news_with_en.description,
            'created_at': self.news_with_en.created_at.strftime('%d/%m/%y'),
            'picture': None,
            'slug': 'second',
        }

    def test_get_single_news_in_english(self):
        response = self.client.get(f'/news/{self.news_with_en.slug}/', {'language': 'en'})
        assert response.status_code == 200, response.status_code
        assert response.json() == {
            'id': self.news_with_en.id,
            'title': self.news_with_en.en_title,
            'description': self.news_with_en.en_description,
            'created_at': self.news_with_en.created_at.strftime('%d/%m/%y'),
            'picture': None,
            'slug': 'second',
        }
