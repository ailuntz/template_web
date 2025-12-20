import { derived, writable } from 'svelte/store';

interface User {
	id: number;
	email: string;
	full_name?: string | null;
	avatar?: string | null;
	is_active: boolean;
	created_at?: string;
	updated_at?: string;
}

interface AuthState {
	user: User | null;
	token: string | null;
	refreshToken: string | null;
	loading: boolean;
	initialized: boolean;
}

const USER_CACHE_KEY = 'cached_user';

function createAuthStore() {
	const { subscribe, set, update } = writable<AuthState>({
		user: null,
		token: null,
		refreshToken: null,
		loading: true,
		initialized: false,
	});

	return {
		subscribe,
		setUser: (user: User | null) => {
			if (user) {
				localStorage.setItem(USER_CACHE_KEY, JSON.stringify(user));
			} else {
				localStorage.removeItem(USER_CACHE_KEY);
			}
			update((state) => ({ ...state, user, loading: false }));
		},
		setToken: (accessToken: string | null, refreshToken: string | null) => {
			if (accessToken) {
				localStorage.setItem('access_token', accessToken);
			} else {
				localStorage.removeItem('access_token');
			}

			if (refreshToken) {
				localStorage.setItem('refresh_token', refreshToken);
			} else {
				localStorage.removeItem('refresh_token');
			}

			update((state) => ({ ...state, token: accessToken, refreshToken }));
		},
		login: (user: User, accessToken: string, refreshToken: string) => {
			localStorage.setItem('access_token', accessToken);
			localStorage.setItem('refresh_token', refreshToken);
			localStorage.setItem(USER_CACHE_KEY, JSON.stringify(user));
			set({ user, token: accessToken, refreshToken, loading: false, initialized: true });
		},
		logout: () => {
			localStorage.removeItem('access_token');
			localStorage.removeItem('refresh_token');
			localStorage.removeItem(USER_CACHE_KEY);
			set({ user: null, token: null, refreshToken: null, loading: false, initialized: true });
		},
		initialize: () => {
			const token = localStorage.getItem('access_token');
			const refreshToken = localStorage.getItem('refresh_token');
			const cachedUser = localStorage.getItem(USER_CACHE_KEY);
			let user: User | null = null;

			if (cachedUser) {
				try {
					user = JSON.parse(cachedUser);
				} catch {
					localStorage.removeItem(USER_CACHE_KEY);
				}
			}

			update((state) => ({
				...state,
				token,
				refreshToken,
				user,
				loading: !!token && !user,
				initialized: true,
			}));
			return token;
		},
		setLoading: (loading: boolean) => {
			update((state) => ({ ...state, loading }));
		},
	};
}

export const auth = createAuthStore();

export const isAuthenticated = derived(auth, ($auth) => !!$auth.user);
export const currentUser = derived(auth, ($auth) => $auth.user);
export const isLoading = derived(auth, ($auth) => $auth.loading);
