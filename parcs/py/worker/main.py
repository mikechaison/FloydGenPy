import logging
import time
from parcs.server import Service, serve

def update_row(i, k, n, row_i, row_k):
    for j in range(n):
        row_i[j] = min(row_i[j], row_i[k] + row_k[j])
    return row_i

class Worker(Service):
    def run(self):
        while True:
            tasks = self.recv()
                
            k = tasks[0][1]
            a = tasks[0][0]
            b = tasks[-1][0]
            logging.info(f'Calculating paths through vertex {k} from vertices between {a} and {b}')
            
            rows = []
            for task in tasks:
                new_row = update_row(*task)
                rows.append(new_row)

            self.send(rows) 
            logging.info(f'Iteration {k} from vertices between {a} and {b} finished and sent.')

serve(Worker())