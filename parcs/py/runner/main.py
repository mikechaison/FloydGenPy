import os
import time
import logging
import json
from parcs.server import Runner, serve

def split(all_tasks, n, p):
    size = n // p
    rem = n % p
    splitted = []
    start = 0
    for i in range(p):
        end = start + size + (1 if i < rem else 0)
        splitted.append(all_tasks[start:end])
        start = end
    return splitted

class Leader(Runner):
    def run(self):
        n = int(os.environ.get('N', 100))
        w = int(os.getenv('WORKERS', 2))
        service_image = os.getenv('SERVICE_IMAGE')
        
        logging.info(f'Starting Leader: N={n}, WORKERS={w}')

        try:
            with open('./matrix.json', 'r') as f:
                dist = json.load(f)
            logging.info('matrix.json loaded successfully')
        except FileNotFoundError:
            logging.error('Error: matrix.json not found!')
            return

        workers = [None] * w
        for i in range(w):
            workers[i] = self.engine.run(service_image)
        
        start_time = time.time()

        for k in range(n):
            logging.info(f'Iteration {k}')
            all_tasks = [(i, k, n, dist[i], dist[k]) for i in range(n)]
            splitted_tasks = split(all_tasks, n, w)
            
            tasks = []
            for i in range(w):
                t = workers[i]
                t.send_all(splitted_tasks[i])
                tasks.append(t)
            
            res = []
            for t in tasks:
                res += t.recv()
            dist = res
        
        end_time = time.time()
        logging.info('Task finished!')
        logging.info(f'Total computation time: {end_time - start_time}')

        for worker in workers:
            worker.shutdown()

        with open('output/result.json', 'w') as f:
            json.dump(dist, f)
        
        logging.info('File result.json saved successfully!')
        logging.info("Keeping container alive for 5 minutes...")
        time.sleep(300)

serve(Leader())