import pytest
from django.shortcuts import resolve_url
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.testapp.models import Animal


@pytest.fixture
def animals(db):
    return [
        Animal.objects.create(name=f"animal {i}", bio="is fun")
        for i in range(2)
    ]


class TestsMixin:
    def get_total_forms(self, prefix, container):
        return container.find_element_by_css_selector(
            f"#id_{prefix}-TOTAL_FORMS").get_attribute("value")

    def get_min_num_forms(self, prefix, container):
        return container.find_element_by_id(
            f"id_{prefix}-MIN_NUM_FORMS").get_attribute("value")

    def get_max_num_forms(self, prefix, container):
        return container.find_element_by_id(
            f"id_{prefix}-MAX_NUM_FORMS").get_attribute("value")

    def get_forms(self, container):
        return container.find_elements_by_css_selector("[formset-form]")


class TestFormset(TestsMixin):
    url = resolve_url('formset')

    def test_add_formset(self, live_server, driver):
        driver.get(live_server.url + self.url)
        prefix = "animal1"

        # get container by prefix
        container = driver.find_element_by_id(prefix)
        btn = container.find_element_by_css_selector("[formset-add]")

        # clicking in add button
        btn.click()
        btn.click()

        # get total_forms
        total_forms = self.get_total_forms(prefix, container)
        forms = container.find_elements_by_css_selector(
            "[formset-form]")
        assert total_forms == "2"
        assert len(forms) == 2

        first_form = forms[0]
        second_form = forms[1]

        assert first_form.find_element_by_id(f"id_{prefix}-0-name")
        assert first_form.find_element_by_id(f"id_{prefix}-0-bio")
        assert second_form.find_element_by_id(f"id_{prefix}-1-name")
        assert second_form.find_element_by_id(f"id_{prefix}-1-bio")

    def test_delete_form_in_formset(self, live_server, driver):
        driver.get(live_server.url + self.url)
        prefix = "animal1"
        container = driver.find_element_by_id(prefix)
        btn = container.find_element_by_css_selector("[formset-add]")

        # clicking in add button
        btn.click()
        btn.click()
        btn.click()

        _, form2, _ = self.get_forms(container)

        # find delete button
        del_btn = form2.find_element_by_css_selector("[formset-form-delete]")

        # delete form
        del_btn.click()

        forms = self.get_forms(container)
        assert len(forms) == 2

        first_form = forms[0]
        second_form = forms[1]
        assert first_form.find_element_by_id(f"id_{prefix}-0-name")
        assert first_form.find_element_by_id(f"id_{prefix}-0-bio")
        assert first_form.find_element_by_id(f"id_{prefix}-0-DELETE")\
            .get_attribute("hidden")
        assert second_form.find_element_by_id(f"id_{prefix}-1-name")
        assert second_form.find_element_by_id(f"id_{prefix}-1-bio")
        assert second_form.find_element_by_id(f"id_{prefix}-1-DELETE")\
            .get_attribute("hidden")

    def test_undelete_with_min_num(self, live_server, driver):
        driver.get(live_server.url + self.url)
        prefix = "animal2"
        container = driver.find_element_by_id(prefix)

        min_num = self.get_min_num_forms(prefix, container)
        assert min_num == '1'

        form1, form2 = self.get_forms(container)

        form1.find_element_by_css_selector("[formset-form-delete]").click()
        form2.find_element_by_css_selector("[formset-form-delete]").click()

        total_forms = self.get_total_forms(prefix, container)
        assert total_forms == '1'
        assert len(self.get_forms(container)) == 1

    def test_unadded_with_max_num(self, live_server, driver):
        driver.get(live_server.url + self.url)
        prefix = "animal2"
        container = driver.find_element_by_id(prefix)

        max_num = self.get_max_num_forms(prefix, container)
        assert max_num == '4'

        btn = container.find_element_by_css_selector("[formset-add]")

        # clicking in add button
        btn.click()
        btn.click()
        btn.click()
        btn.click()

        total_forms = self.get_total_forms(prefix, container)
        assert total_forms == '4'
        assert len(self.get_forms(container)) == 4

    def test_hidden_delete(self, live_server, driver):
        driver.get(live_server.url + self.url)
        prefix = "animal3"
        container = driver.find_element_by_id(prefix)

        totals_num = self.get_total_forms(prefix, container)
        assert totals_num == '2'

        form1, form2 = self.get_forms(container)
        btn1 = form1.find_element_by_css_selector("[formset-form-delete]")
        btn2 = form2.find_element_by_css_selector("[formset-form-delete]")

        assert btn1.get_attribute("hidden")
        assert btn2.get_attribute("hidden")


class TestModelFormset(TestsMixin):
    url = resolve_url("modelformset")

    def test_delete_with_id_filled(self, live_server, driver, animals):
        driver.get(live_server.url + self.url)
        prefix = "animal1"
        container = driver.find_element_by_id(prefix)

        form1, form2, form3 = self.get_forms(container)
        btn1 = form1.find_element_by_css_selector("[formset-form-delete]")
        btn2 = form2.find_element_by_css_selector("[formset-form-delete]")
        btn3 = form3.find_element_by_css_selector("[formset-form-delete]")

        btn1.click()
        btn2.click()
        btn3.click()

        assert self.get_total_forms(prefix, container) == '2'

        form1, form2 = container.find_elements_by_css_selector(
            "[formset-form-excluded]"
        )
        chk1 = form1.find_element_by_css_selector("[name$=-DELETE]")
        chk2 = form2.find_element_by_css_selector("[name$=-DELETE]")
        assert chk1.get_attribute("checked") == "true"
        assert chk2.get_attribute("checked") == "true"

        restore_link = (
            WebDriverWait(driver, 60).until(
                expected_conditions.presence_of_element_located(
                    (By.CSS_SELECTOR, "[formset-undo]")
                )
            )
        )
        restore_link.click()

        excluded_forms = container.find_elements_by_css_selector(
            "[formset-form-excluded]"
        )
        forms = self.get_forms(container)
        assert len(excluded_forms) == 1
        assert len(forms) == 1

        form1 = forms[0]
        chk1 = form1.find_element_by_css_selector("[name$=-DELETE]")
        assert chk1.get_attribute("checked") is None


class TestModelFormsetSubmit(TestsMixin):
    url = resolve_url("modelformset2")

    def test_submit_delete(self, live_server, driver, animals):
        driver.get(live_server.url + self.url)
        prefix = "animal"
        container = driver.find_element_by_id(prefix)

        form1, form2 = self.get_forms(container)
        btn1 = form1.find_element_by_css_selector("[formset-form-delete]")
        btn2 = form2.find_element_by_css_selector("[formset-form-delete]")

        btn1.click()
        btn2.click()

        btn_submit = driver.find_element_by_id("btn-submit")
        btn_submit.click()

        container = driver.find_element_by_id(prefix)
        forms = self.get_forms(container)
        assert len(forms) == 0
