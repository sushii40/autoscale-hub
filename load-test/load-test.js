import http from 'k6/http';
import { check, sleep } from 'k6';

// BASE_URL is read from the environment variable (e.g., $env:BASE_URL="http://127.0.0.1:54321")
// Fallback defaults to http://127.0.0.1:5000 if not set.
const BASE_URL = (__ENV.BASE_URL || 'http://127.0.0.1:5000').replace(/\/+$/, '');

export const options = {
  stages: [
    { duration: '30s', target: 20 },   // Warm-up ramp-up to 20 virtual users
    { duration: '60s', target: 100 },  // Ramp-up to 100 users to trigger HPA scaling (CPU > 50%)
    { duration: '60s', target: 100 },  // Sustained peak load at 100 users
    { duration: '30s', target: 0 },    // Ramp-down to 0 to observe cooldown and scale-down
  ],
  thresholds: {
    http_req_failed: ['rate<0.05'],    // Less than 5% error rate
    http_req_duration: ['p(95)<2000'], // 95% of requests within 2 seconds
  },
};

export default function () {
  // Hit the CPU-intensive /stress endpoint designed specifically for HPA load testing
  const url = `${BASE_URL}/stress`;
  const response = http.get(url, {
    tags: { name: 'GetStress' },
  });

  check(response, {
    'status is 200': (r) => r.status === 200,
    'status completed in payload': (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.status === 'completed';
      } catch (e) {
        return false;
      }
    },
  });

  // Short delay to avoid client-side socket saturation while keeping CPU hot
  sleep(0.1);
}
