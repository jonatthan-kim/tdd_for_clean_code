# 기능 테스트를 담고 있는 파일.
import sys, os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

class NewVisitorTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server_url = os.environ.get('URL', cls.live_server_url)

    @classmethod
    def tearDownClass(cls):
        if cls.server_url == cls.live_server_url:
            super().tearDownClass()

    def setUp(self):
        self.browser = webdriver.Chrome()  # source ~/.bash_profile을 해주지 않으면 다음 에러 발생. selenium.common.exceptions.WebDriverException: Message: 'chromedriver' executable needs to be in PATH.
        self.browser.implicitly_wait(3)  # 암묵적 대기

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):
        self.browser.get(self.server_url)  # runserver를 하지 않으면 이 지점에서 에러가 발생함.

        # 웹 페이지 타이틀과 헤더가 'To-Do'를 표시하고 있음
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text  # find_element_by_*는 deprecated라고 함. 나중에 이것들 다 바꿔줘야함.
        # header_text = self.browser.find_element('h1').text
        self.assertIn('To-Do', header_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            '작업 아이템 입력'
        )

        # "공작깃털 사기"라고 텍스트 상자에 입력
        inputbox.send_keys('공작깃털 사기')
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        # 엔터키를 치면 페이지가 갱신되고 작업 목록에 "1: 공작깃털 사기" 아이템이 추가됨.

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재
        # 다시 "공작깃털을 이용해서 그물 만들기"라고 입력한다
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
        inputbox.send_keys(Keys.ENTER)

        # 페이지는 다시 갱신되고, 두 개의 아이템이 목록에 보인다
        self.check_for_row_in_list_table('1: 공작깃털 사기')
        self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')

        ## 새로운 사용자인 프란시스가 사이트에 접속
        ## 새로운 브라우저 세션을 이용해서 에디스의 정보가 쿠키를 통해 유입되는 것을 방지. 이중#은 메타 주석. 테스트가 어떻게 동작하는지 설명하기 위해 사용.
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # 프란시스가 홈페이지에 접속한다
        # 에디스의 리스트는 보이지 않음.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertNotIn('그물 만들기', page_text)

        # 프란시스가 새로운 아이템을 입력하기 시작.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('우유 사기')
        inputbox.send_keys(Keys.ENTER)

        # 프란시스가 전용 url을 취득
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 에디스가 입력한 흔적이 없다는 것을 다시 확인
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('공작깃털 사기', page_text)
        self.assertIn('우유 사기', page_text)

    def test_layout_and_styling(self):
        # 에디스는 메인 페이지를 방문한다
        self.browser.get(self.server_url)
        self.browser.set_window_size(1024, 768)

        # 그녀는 입력 상자가 가운데 배치된 것을 본다
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10
        )

        inputbox.send_keys('testing\n')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=10
        )
