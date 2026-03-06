import { z } from 'zod';

export const loginSchema = z.object({
	email: z.string().email('请输入有效的邮箱地址'),
	password: z.string().min(6, '密码至少6个字符'),
});

export const registerSchema = z
	.object({
		email: z.string().email('请输入有效的邮箱地址'),
		institution_code: z
			.string()
			.regex(/^\d{6}$/, '请输入 6 位机构验证码'),
		full_name: z.string().min(2, '姓名至少2个字符').optional(),
		password: z
			.string()
			.min(8, '密码至少8个字符')
			.regex(/[A-Za-z]/, '密码必须包含至少一个字母')
			.regex(/\d/, '密码必须包含至少一个数字'),
		confirmPassword: z.string().min(8, '密码至少8个字符'),
	})
	.refine((data) => data.password === data.confirmPassword, {
		message: '两次密码不一致',
		path: ['confirmPassword'],
	});

export type LoginInput = z.infer<typeof loginSchema>;
export type RegisterInput = z.infer<typeof registerSchema>;
