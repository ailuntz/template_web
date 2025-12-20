import { goto } from '$app/navigation';
import { browser } from '$app/environment';
import { client } from './generated';

// API 基础 URL：生产环境从环境变量获取，开发环境使用相对路径（通过 Vite 代理）
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

// Share the generated client so SDK functions use the same config/interceptors
client.setConfig({
	baseUrl: API_BASE_URL,
});

// Add auth token interceptor
client.interceptors.request.use((request) => {
	if (browser) {
		const token = localStorage.getItem('access_token');
		if (token) {
			request.headers.set('Authorization', `Bearer ${token}`);
		}
	}
	return request;
});

// Refresh token state management
let isRefreshing = false;
let refreshSubscribers: Array<(token: string) => void> = [];
let isRedirectingToLogin = false;

function subscribeTokenRefresh(cb: (token: string) => void) {
	refreshSubscribers.push(cb);
}

function onRefreshed(token: string) {
	refreshSubscribers.forEach((cb) => cb(token));
	refreshSubscribers = [];
}

async function refreshAccessToken(): Promise<string | null> {
	const refreshToken = localStorage.getItem('refresh_token');
	if (!refreshToken) return null;

	try {
		const response = await fetch(`${API_BASE_URL}/api/v1/auth/refresh`, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ refresh_token: refreshToken })
		});

		if (!response.ok) {
			localStorage.removeItem('access_token');
			localStorage.removeItem('refresh_token');
			localStorage.removeItem('cached_user');
			return null;
		}

		const data = await response.json();
		localStorage.setItem('access_token', data.access_token);
		localStorage.setItem('refresh_token', data.refresh_token);
		return data.access_token;
	} catch (error) {
		console.error('Failed to refresh token:', error);
		return null;
	}
}

// Add response interceptor with automatic token refresh
client.interceptors.response.use(async (response, request) => {
	if (!browser) return response;

	const isAuthEndpoint = request.url.includes('/api/v1/auth/');

	if (response.status === 401 && !isAuthEndpoint) {
		if (!isRefreshing) {
			isRefreshing = true;
			const newToken = await refreshAccessToken();
			isRefreshing = false;

			if (newToken) {
				// Refresh succeeded, notify all waiting requests
				onRefreshed(newToken);

				// Retry current request with new token
				request.headers.set('Authorization', `Bearer ${newToken}`);
				return client.request(request);
			} else {
				// Refresh failed, redirect to login
				if (!isRedirectingToLogin) {
					isRedirectingToLogin = true;
					goto('/auth/login').finally(() => {
						isRedirectingToLogin = false;
					});
				}
			}
		} else {
			// Refreshing in progress, wait for it to complete
			return new Promise((resolve) => {
				subscribeTokenRefresh((newToken: string) => {
					request.headers.set('Authorization', `Bearer ${newToken}`);
					resolve(client.request(request));
				});
			});
		}
	}

	return response;
});

export const apiClient = client;
