from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from collections import defaultdict
import json
import random


class RandomHttpProxyMiddleware(HttpProxyMiddleware):
    def __init__(self, auth_encoding='latin-l', proxy_list_file=None):
        if not proxy_list_file:
            raise NotConfigured

        self.auth_encoding = auth_encoding
        # �ֱ��������б�ά�� HTTP �� HTTPS �Ĵ���{'http': [...], 'https': [...]}
        self.proxies = defaultdict(list)

        # �� json �ļ��ж�ȡ�����������Ϣ������ self.proxies
        with open(proxy_list_file) as f:
            proxy_list = json.load(f)
            for proxy in proxy_list:
                scheme = proxy['proxy_scheme']
                url = proxy['proxy']
                self.proxies[scheme].append(self._get_proxy(url,scheme))

    @classmethod
    def from_crawler(cls, crawler):
        # �������ļ��ж�ȡ�û���֤��Ϣ�ı���
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING', 'latin-l')

        # �������ļ��ж�ȡ����������б��ļ���·��
        proxy_list_file = crawler.settings.get('HTTPPROXY_PROXY_LIST_FILE')

        return cls(auth_encoding, proxy_list_file)

    def _set_proxy(self, request, scheme):
        # ���ѡ��һ������
        creds, proxy = random.choice(self.proxies[scheme])
        request.meta['proxy'] = proxy
        if creds:
            request.headers['Proxy-Authorization'] = b'Basic' + creds