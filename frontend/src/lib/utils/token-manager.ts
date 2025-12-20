import { browser } from '$app/environment';

const REFRESH_BEFORE_EXPIRY_MS = 2 * 60 * 1000; // 2 minutes before expiry
const API_BASE_URL = import.meta.env.VITE_API_URL || '';

class TokenManager {
	private refreshTimer: ReturnType<typeof setTimeout> | null = null;

	/**
	 * Decode JWT token and extract expiration time
	 */
	private decodeToken(token: string): { exp: number } | null {
		try {
			const base64Url = token.split('.')[1];
			const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
			const jsonPayload = decodeURIComponent(
				atob(base64)
					.split('')
					.map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
					.join('')
			);
			return JSON.parse(jsonPayload);
		} catch (error) {
			console.error('Failed to decode token:', error);
			return null;
		}
	}

	/**
	 * Refresh the access token
	 */
	private async refreshToken(): Promise<boolean> {
		const refreshToken = localStorage.getItem('refresh_token');
		if (!refreshToken) return false;

		try {
			const response = await fetch(`${API_BASE_URL}/api/v1/auth/refresh`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ refresh_token: refreshToken })
			});

			if (!response.ok) {
				this.stop();
				localStorage.removeItem('access_token');
				localStorage.removeItem('refresh_token');
				localStorage.removeItem('cached_user');
				return false;
			}

			const data = await response.json();
			localStorage.setItem('access_token', data.access_token);
			localStorage.setItem('refresh_token', data.refresh_token);

			// Schedule next refresh
			this.scheduleRefresh(data.access_token);
			return true;
		} catch (error) {
			console.error('Failed to refresh token:', error);
			this.stop();
			return false;
		}
	}

	/**
	 * Schedule token refresh before expiry
	 */
	private scheduleRefresh(accessToken: string) {
		// Clear existing timer
		if (this.refreshTimer) {
			clearTimeout(this.refreshTimer);
			this.refreshTimer = null;
		}

		const payload = this.decodeToken(accessToken);
		if (!payload || !payload.exp) return;

		const now = Date.now();
		const expiryTime = payload.exp * 1000; // Convert to milliseconds
		const timeUntilRefresh = expiryTime - now - REFRESH_BEFORE_EXPIRY_MS;

		if (timeUntilRefresh <= 0) {
			// Token is about to expire or already expired, refresh immediately
			this.refreshToken();
		} else {
			// Schedule refresh before expiry
			this.refreshTimer = setTimeout(() => {
				this.refreshToken();
			}, timeUntilRefresh);
		}
	}

	/**
	 * Start automatic token refresh
	 */
	start() {
		if (!browser) return;

		const accessToken = localStorage.getItem('access_token');
		if (accessToken) {
			this.scheduleRefresh(accessToken);
		}
	}

	/**
	 * Stop automatic token refresh
	 */
	stop() {
		if (this.refreshTimer) {
			clearTimeout(this.refreshTimer);
			this.refreshTimer = null;
		}
	}
}

export const tokenManager = new TokenManager();
