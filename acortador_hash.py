import hashlib
from urllib.parse import urlparse
from base62 import encode, decode

class URLShortener:
    BASE62_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def __init__(self, base_url=None, starting_id =597652313):
        self.base_url = base_url 
        self.current_id = starting_id
        self.database = {}
        self.url_to_id = {}
    
    '''
    def _to_base62(self, num): # Cambiar por pybase62
        if num == 0:
            return self.BASE62_ALPHABET[0]
        
        result = []
        while num > 0:
            result.append(self.BASE62_ALPHABET[num % 62])
            num //= 62
        
        return ''.join(reversed(result))
    
    def _from_base62(self, base62_str):
        num = 0
        for char in base62_str:
            num = num * 62 + self.BASE62_ALPHABET.index(char)
        return num
    '''
    
    def shorten(self, long_url, length=5):
        if not self.base_url:
            url_to_parse = long_url if "://" in long_url else f"http://{long_url}"
            parsed = urlparse(url_to_parse)
            self.base_url = parsed.netloc

        if long_url in self.url_to_id:
            existing_id = self.url_to_id[long_url]
            short_code = self.database[existing_id]['hash']
            return f"{self.base_url}/{short_code}"
        
        current_id = self.current_id
        short_code = encode(current_id)
        #short_code = self._to_base62(current_id)

        self.database[current_id] = {
            'id': current_id,
            'hash': short_code,
            'long_url': long_url
        }
        self.url_to_id[long_url] = current_id
        self.current_id += 1

        #hash_object = hashlib.md5(long_url.encode())
        #hash_int = int(hash_object.hexdigest(), 16)

        #short_code = self._to_base62(hash_int)
        #short_code = short_code[:length]

        return f"{self.base_url}/{short_code}"
    
    def get_long_url(self, short_code):
        decoded_id = decode(short_code)
        # Agregar opción de pybase here.
        if decoded_id in self.database:
            return self.database[decoded_id]['long_url']
        
        return None
    
    def get_stats(self):
        return {
            'total': len(self.database),
            'next_id': self.current_id,
            'database': self.database
        }
    
if __name__ == "__main__":
    shortener = URLShortener()

    long_url1 = "usm.cl/informatica/postulaciones-a-postgrado/2025/magiste-en-ingenieria-informatica/"
    long_url2 = "usm.cl/noticias/2024/evento-importante"
    
    short_url1 = shortener.shorten(long_url1)
    short_url2 = shortener.shorten(long_url2)

    hash1 = short_url1.split('/')[-1]
    print(shortener.get_long_url(hash1))
    
    print(f"Long URL 1: {long_url1}")
    print(f"Short URL 1: {short_url1}")
    print(f"\nLong URL 2: {long_url2}")
    print(f"Short URL 2: {short_url2}")
    
    print(f"\nDatabase stats: {shortener.get_stats()}")