// 🏆 Service Worker المپیکی - برای Progressive Web App
const CACHE_NAME = 'natiq-olympic-v3.0.0';
const CACHE_FILES = [
  '/',
  '/index.html',
  '/manifest.json',
  'https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap',
  'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css',
  'https://cdn.jsdelivr.net/npm/chart.js'
];

// نصب Service Worker
self.addEventListener('install', (event) => {
  console.log('🏆 Installing Olympic Service Worker...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('📦 Caching Olympic assets');
        return cache.addAll(CACHE_FILES);
      })
      .then(() => {
        console.log('✅ Olympic Service Worker installed');
        return self.skipWaiting();
      })
  );
});

// فعال‌سازی Service Worker
self.addEventListener('activate', (event) => {
  console.log('🚀 Activating Olympic Service Worker...');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log(`🗑️ Deleting old cache: ${cacheName}`);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('✅ Olympic Service Worker activated');
      return self.clients.claim();
    })
  );
});

// هندل درخواست‌ها
self.addEventListener('fetch', (event) => {
  const request = event.request;
  
  // فقط هندل درخواست‌های GET
  if (request.method !== 'GET') return;
  
  // API requests - Network First
  if (request.url.includes('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // کش پاسخ API
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseClone);
          });
          return response;
        })
        .catch(() => {
          // Fallback to cache if network fails
          return caches.match(request);
        })
    );
  } else {
    // Static assets - Cache First
    event.respondWith(
      caches.match(request)
        .then((cachedResponse) => {
          if (cachedResponse) {
            // به‌روزرسانی کش در پس‌زمینه
            event.waitUntil(
              fetch(request).then((response) => {
                return caches.open(CACHE_NAME).then((cache) => {
                  return cache.put(request, response);
                });
              })
            );
            return cachedResponse;
          }
          
          // اگر در کش نبود، از شبکه بگیر
          return fetch(request)
            .then((response) => {
              // در کش ذخیره کن
              const responseClone = response.clone();
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(request, responseClone);
              });
              return response;
            })
            .catch(() => {
              // Fallback برای آفلاین
              if (request.url.includes('.html')) {
                return caches.match('/');
              }
              return new Response('🚀 Olympic System - Offline Mode', {
                headers: { 'Content-Type': 'text/plain' }
              });
            });
        })
    );
  }
});

// هندل push notifications
self.addEventListener('push', (event) => {
  const data = event.data.json();
  
  const options = {
    body: data.body,
    icon: '/icon-192.png',
    badge: '/badge-72.png',
    vibrate: [100, 50, 100],
    data: {
      url: data.url || '/'
    },
    actions: [
      {
        action: 'open',
        title: 'باز کردن'
      },
      {
        action: 'close',
        title: 'بستن'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(data.title, options)
  );
});

// هندل کلیک روی notification
self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  
  if (event.action === 'open') {
    event.waitUntil(
      clients.openWindow(event.notification.data.url)
    );
  }
});

// هندل background sync
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-messages') {
    event.waitUntil(syncMessages());
  }
});

async function syncMessages() {
  // منطق همگام‌سازی پیام‌های آفلاین
  console.log('🔄 Syncing offline messages...');
}
