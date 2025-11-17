import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  vus: 20,
  duration: '30s'
};

export default function () {
  const url = 'http://localhost:8080/api/test';

  // Slowloris-style header drip
  const params = {
    headers: {
      'Content-Type': 'application/json',
      'X-Fuzz': 'slowloris'
    },
    timeout: '5s'
  };

  http.post(url, JSON.stringify({ fuzz: "test" }), params);

  // Burst requests for rate-limit fuzzing
  for (let i = 0; i < 20; i++) {
    http.get(url);
  }

  sleep(1);
}
