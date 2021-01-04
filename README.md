This is a reference application showcasing how to mix Django an Vue.

It relies on Django, Vue, django-compressor-parceljs, and Axios.

Pull requests are more than welcome - I'm trying to establish some best practices for my projects. All inputs and pointers are welcome!

Checkout `docs/` for in-depth documentation.

# How to use

I generally do the following:

1. Clone repo: `git@github.com:e8johan/django-vue-example.git`
2. Enter repo directory: `cd django-vue-example`
3. Create a Python venv: `python3 -m venv venv`
4. Activate Python venv: `source venv/bin/activate`
5. Install Python requirements: `pip install -r requirements.txt`
6. Install npm requirements: `npm install`
7. Source npm bin path magic fix: `source source-to-set-path.sh`
8. Run server in development mode: `NODE_ENV=development ./manage.py runserver`

# Open Issues

- Describe how to setup unit-testing for Django
- Describe how to setup unit-testing for Vue app
- Describe how to deploy
- Describe how to setup CI/CD
