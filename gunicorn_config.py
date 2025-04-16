from app import post_worker_init

workers = 4
worker_class = 'sync'
timeout = 120
preload_app = False

post_worker_init = post_worker_init