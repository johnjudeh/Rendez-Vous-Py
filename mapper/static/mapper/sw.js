const staticCacheName = 'rendezvous-static-v1';
const cacheWhiteList = [ staticCacheName ];
const STATIC_PREFIX = '/static/mapper'

// Event fires when service worker is first discovered
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(staticCacheName).then(cache => {
      return cache.addAll([
        '/',
        // TODO: Come back to fix these rotues once authentication is added
        // '/register',
        // '/login',
        STATIC_PREFIX + '/manifest.json',
        STATIC_PREFIX + '/js/maps.js',
        STATIC_PREFIX + '/js/register.js',
        STATIC_PREFIX + '/js/sw/index.js',
        STATIC_PREFIX + '/js/manup.min.js',
        STATIC_PREFIX + '/js/pwa-nav.js',
        STATIC_PREFIX + '/css/app.css',
        STATIC_PREFIX + '/avatars/male.png',
        STATIC_PREFIX + '/avatars/female.png',
        STATIC_PREFIX + '/avatars/ninja.png',
        'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.13/semantic.min.css',
        'https://fonts.googleapis.com/css?family=Oleo+Script+Swash+Caps|Roboto:400,400i,500,700,700i',
        'https://code.jquery.com/jquery-3.2.1.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.2.13/semantic.js'
      ]);
    })
  );
});

// Event fires when new sw is intalled and ready to take over page
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return cacheNames.filter(cacheName => {
        return !cacheWhiteList.includes(cacheName);
      }).map(cacheName => {
        console.log('Deleting:', cacheName);
        return caches.delete(cacheName);
      })
    })
  );
})

// Handles how a page makes fetch requests
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.open(staticCacheName).then(cache => {

      // Searchs for respone in cache
      return cache.match(event.request).then(response => {

        // Ensures that no-cache resources are checked with server
        if (response && response.headers.has('cache-control')) {
          if (response.headers.get('cache-control') === 'no-cache') {
            return fetch(event.request).then((networkResponse) => {

              // Updates cache with fresh response
              cache.put(event.request, networkResponse.clone());
              return networkResponse;

            // In case of errors in Fetch
            }).catch(() => {
              return response;
            });
          }
        }
        // Do not need updating as they are static
        return response || fetch(event.request);
      })
    })
  );
})

// Awaits message to update service worker
self.addEventListener('message', (event) => {
  if (event.data.action === 'skipWaiting') {
    self.skipWaiting();
  }
})
