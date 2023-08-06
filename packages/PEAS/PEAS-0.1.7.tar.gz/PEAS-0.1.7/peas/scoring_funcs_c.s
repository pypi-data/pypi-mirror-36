	.file	"scoring_funcs_c.c"
	.text
	.globl	c_compute_sum_table_2d
	.type	c_compute_sum_table_2d, @function
c_compute_sum_table_2d:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$96, %rsp
	movq	%rdi, -56(%rbp)
	movq	%rsi, -64(%rbp)
	movq	%rdx, -72(%rbp)
	movq	%rcx, -80(%rbp)
	movq	%r8, -88(%rbp)
	movq	-64(%rbp), %rdx
	movq	-64(%rbp), %rcx
	movq	-88(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	get_row_ptrs
	movq	%rax, -24(%rbp)
	movq	-64(%rbp), %rdx
	movq	-64(%rbp), %rcx
	movq	-56(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	get_row_ptrs
	movq	%rax, -32(%rbp)
	movq	-72(%rbp), %rax
	movq	%rax, -16(%rbp)
	jmp	.L2
.L6:
	movq	$0, -8(%rbp)
	jmp	.L3
.L5:
	movq	-16(%rbp), %rax
	movq	-8(%rbp), %rdx
	addq	%rdx, %rax
	movq	%rax, -40(%rbp)
	movq	-8(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-40(%rbp), %rdx
	salq	$3, %rdx
	addq	%rax, %rdx
	movl	$0, %eax
	movq	%rax, (%rdx)
	movq	-8(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-40(%rbp), %rdx
	salq	$3, %rdx
	addq	%rdx, %rax
	movq	-8(%rbp), %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-24(%rbp), %rdx
	addq	%rcx, %rdx
	movq	(%rdx), %rdx
	movq	-40(%rbp), %rcx
	salq	$3, %rcx
	addq	%rcx, %rdx
	movsd	(%rdx), %xmm1
	movq	-8(%rbp), %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-32(%rbp), %rdx
	addq	%rcx, %rdx
	movq	(%rdx), %rdx
	movq	-40(%rbp), %rcx
	salq	$3, %rcx
	addq	%rcx, %rdx
	movsd	(%rdx), %xmm0
	addsd	%xmm1, %xmm0
	movsd	%xmm0, (%rax)
	movq	-16(%rbp), %rax
	cmpq	-72(%rbp), %rax
	je	.L4
	movq	-8(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-40(%rbp), %rdx
	salq	$3, %rdx
	addq	%rdx, %rax
	movq	-8(%rbp), %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-24(%rbp), %rdx
	addq	%rcx, %rdx
	movq	(%rdx), %rdx
	movq	-40(%rbp), %rcx
	salq	$3, %rcx
	addq	%rcx, %rdx
	movsd	(%rdx), %xmm1
	movq	-8(%rbp), %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-24(%rbp), %rdx
	addq	%rcx, %rdx
	movq	(%rdx), %rdx
	movq	-40(%rbp), %rcx
	salq	$3, %rcx
	subq	$8, %rcx
	addq	%rcx, %rdx
	movsd	(%rdx), %xmm0
	addsd	%xmm1, %xmm0
	movsd	%xmm0, (%rax)
	movq	-8(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-40(%rbp), %rdx
	salq	$3, %rdx
	addq	%rdx, %rax
	movq	-8(%rbp), %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-24(%rbp), %rdx
	addq	%rcx, %rdx
	movq	(%rdx), %rdx
	movq	-40(%rbp), %rcx
	salq	$3, %rcx
	addq	%rcx, %rdx
	movsd	(%rdx), %xmm1
	movq	-8(%rbp), %rdx
	addq	$1, %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-24(%rbp), %rdx
	addq	%rcx, %rdx
	movq	(%rdx), %rdx
	movq	-40(%rbp), %rcx
	salq	$3, %rcx
	addq	%rcx, %rdx
	movsd	(%rdx), %xmm0
	addsd	%xmm1, %xmm0
	movsd	%xmm0, (%rax)
	movq	-72(%rbp), %rax
	movq	-16(%rbp), %rdx
	subq	%rax, %rdx
	movq	%rdx, %rax
	cmpq	$1, %rax
	jbe	.L4
	movq	-8(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-40(%rbp), %rdx
	salq	$3, %rdx
	addq	%rdx, %rax
	movq	-8(%rbp), %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-24(%rbp), %rdx
	addq	%rcx, %rdx
	movq	(%rdx), %rdx
	movq	-40(%rbp), %rcx
	salq	$3, %rcx
	addq	%rcx, %rdx
	movsd	(%rdx), %xmm0
	movq	-8(%rbp), %rdx
	addq	$1, %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-24(%rbp), %rdx
	addq	%rcx, %rdx
	movq	(%rdx), %rdx
	movq	-40(%rbp), %rcx
	salq	$3, %rcx
	subq	$8, %rcx
	addq	%rcx, %rdx
	movsd	(%rdx), %xmm1
	subsd	%xmm1, %xmm0
	movsd	%xmm0, (%rax)
.L4:
	addq	$1, -8(%rbp)
.L3:
	movq	-16(%rbp), %rax
	movq	-64(%rbp), %rdx
	subq	%rax, %rdx
	movq	%rdx, %rax
	cmpq	-8(%rbp), %rax
	ja	.L5
	addq	$1, -16(%rbp)
.L2:
	movq	-16(%rbp), %rax
	cmpq	-80(%rbp), %rax
	jb	.L6
	movq	-32(%rbp), %rax
	movq	%rax, %rdi
	call	free
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	call	free
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	c_compute_sum_table_2d, .-c_compute_sum_table_2d
	.globl	c_compute_sum_table_2d_shuffled
	.type	c_compute_sum_table_2d_shuffled, @function
c_compute_sum_table_2d_shuffled:
.LFB1:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%r12
	pushq	%rbx
	addq	$-128, %rsp
	.cfi_offset 12, -24
	.cfi_offset 3, -32
	movq	%rdi, -104(%rbp)
	movq	%rsi, -112(%rbp)
	movq	%rdx, -120(%rbp)
	movq	%rcx, -128(%rbp)
	movq	%r8, -136(%rbp)
	movq	%rsp, %rax
	movq	%rax, %rbx
	movq	-112(%rbp), %rax
	movq	%rax, %rdx
	subq	$1, %rdx
	movq	%rdx, -56(%rbp)
	movq	%rax, %r11
	movl	$0, %r12d
	movq	%rax, %r9
	movl	$0, %r10d
	salq	$3, %rax
	leaq	7(%rax), %rdx
	movl	$16, %eax
	subq	$1, %rax
	addq	%rdx, %rax
	movl	$16, %esi
	movl	$0, %edx
	divq	%rsi
	imulq	$16, %rax, %rax
	subq	%rax, %rsp
	movq	%rsp, %rax
	addq	$7, %rax
	shrq	$3, %rax
	salq	$3, %rax
	movq	%rax, -64(%rbp)
	movq	$0, -48(%rbp)
	jmp	.L9
.L10:
	movq	-64(%rbp), %rax
	movq	-48(%rbp), %rdx
	movq	-48(%rbp), %rcx
	movq	%rcx, (%rax,%rdx,8)
	addq	$1, -48(%rbp)
.L9:
	movq	-48(%rbp), %rax
	cmpq	-112(%rbp), %rax
	jb	.L10
	movq	-64(%rbp), %rax
	movq	-112(%rbp), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	shuffle_array_st
	movq	-112(%rbp), %rdx
	movq	-112(%rbp), %rcx
	movq	-136(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	get_row_ptrs
	movq	%rax, -72(%rbp)
	movq	-112(%rbp), %rdx
	movq	-112(%rbp), %rcx
	movq	-104(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	get_row_ptrs
	movq	%rax, -80(%rbp)
	movq	-120(%rbp), %rax
	movq	%rax, -32(%rbp)
	jmp	.L11
.L15:
	movq	$0, -24(%rbp)
	jmp	.L12
.L14:
	movq	-32(%rbp), %rax
	movq	-24(%rbp), %rdx
	addq	%rdx, %rax
	movq	%rax, -88(%rbp)
	movq	-64(%rbp), %rax
	movq	-24(%rbp), %rdx
	movq	(%rax,%rdx,8), %rax
	leaq	0(,%rax,8), %rdx
	movq	-80(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rcx
	movq	-64(%rbp), %rax
	movq	-88(%rbp), %rdx
	movq	(%rax,%rdx,8), %rax
	salq	$3, %rax
	addq	%rcx, %rax
	movq	(%rax), %rax
	movq	%rax, -40(%rbp)
	movq	-32(%rbp), %rax
	cmpq	-120(%rbp), %rax
	je	.L13
	movq	-24(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-72(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-88(%rbp), %rdx
	salq	$3, %rdx
	subq	$8, %rdx
	addq	%rdx, %rax
	movsd	(%rax), %xmm0
	movsd	-40(%rbp), %xmm1
	addsd	%xmm1, %xmm0
	movsd	%xmm0, -40(%rbp)
	movq	-24(%rbp), %rax
	addq	$1, %rax
	leaq	0(,%rax,8), %rdx
	movq	-72(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-88(%rbp), %rdx
	salq	$3, %rdx
	addq	%rdx, %rax
	movsd	(%rax), %xmm0
	movsd	-40(%rbp), %xmm1
	addsd	%xmm1, %xmm0
	movsd	%xmm0, -40(%rbp)
	movq	-120(%rbp), %rax
	movq	-32(%rbp), %rdx
	subq	%rax, %rdx
	movq	%rdx, %rax
	cmpq	$1, %rax
	jbe	.L13
	movq	-24(%rbp), %rax
	addq	$1, %rax
	leaq	0(,%rax,8), %rdx
	movq	-72(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-88(%rbp), %rdx
	salq	$3, %rdx
	subq	$8, %rdx
	addq	%rdx, %rax
	movsd	(%rax), %xmm1
	movsd	-40(%rbp), %xmm0
	subsd	%xmm1, %xmm0
	movsd	%xmm0, -40(%rbp)
.L13:
	movq	-24(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-72(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-88(%rbp), %rdx
	salq	$3, %rdx
	addq	%rax, %rdx
	movq	-40(%rbp), %rax
	movq	%rax, (%rdx)
	addq	$1, -24(%rbp)
.L12:
	movq	-32(%rbp), %rax
	movq	-112(%rbp), %rdx
	subq	%rax, %rdx
	movq	%rdx, %rax
	cmpq	-24(%rbp), %rax
	ja	.L14
	addq	$1, -32(%rbp)
.L11:
	movq	-32(%rbp), %rax
	cmpq	-128(%rbp), %rax
	jb	.L15
	movq	-80(%rbp), %rax
	movq	%rax, %rdi
	call	free
	movq	-72(%rbp), %rax
	movq	%rax, %rdi
	call	free
	nop
	movq	%rbx, %rsp
	leaq	-16(%rbp), %rsp
	popq	%rbx
	popq	%r12
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	c_compute_sum_table_2d_shuffled, .-c_compute_sum_table_2d_shuffled
	.globl	generate_2d_denominator_table
	.type	generate_2d_denominator_table, @function
generate_2d_denominator_table:
.LFB2:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$80, %rsp
	movq	%rdi, -56(%rbp)
	movq	%rsi, -64(%rbp)
	movq	%rdx, -72(%rbp)
	movq	%rcx, -80(%rbp)
	movq	-56(%rbp), %rdx
	movq	-56(%rbp), %rcx
	movq	-80(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	get_row_ptrs
	movq	%rax, -32(%rbp)
	movl	$0, %eax
	movq	%rax, -8(%rbp)
	movq	-64(%rbp), %rax
	movq	%rax, -16(%rbp)
	jmp	.L18
.L23:
	movq	-64(%rbp), %rax
	movq	-16(%rbp), %rdx
	subq	%rax, %rdx
	movq	%rdx, %rax
	addq	$1, %rax
	testq	%rax, %rax
	js	.L19
	cvtsi2sdq	%rax, %xmm0
	jmp	.L20
.L19:
	movq	%rax, %rdx
	shrq	%rdx
	andl	$1, %eax
	orq	%rax, %rdx
	cvtsi2sdq	%rdx, %xmm0
	addsd	%xmm0, %xmm0
.L20:
	movsd	-8(%rbp), %xmm1
	addsd	%xmm1, %xmm0
	movsd	%xmm0, -8(%rbp)
	movq	$0, -24(%rbp)
	jmp	.L21
.L22:
	movq	-16(%rbp), %rax
	movq	-24(%rbp), %rdx
	addq	%rdx, %rax
	movq	%rax, -40(%rbp)
	movq	-24(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-32(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-40(%rbp), %rdx
	salq	$3, %rdx
	addq	%rax, %rdx
	movq	-8(%rbp), %rax
	movq	%rax, (%rdx)
	addq	$1, -24(%rbp)
.L21:
	movq	-16(%rbp), %rax
	movq	-56(%rbp), %rdx
	subq	%rax, %rdx
	movq	%rdx, %rax
	cmpq	-24(%rbp), %rax
	ja	.L22
	addq	$1, -16(%rbp)
.L18:
	movq	-16(%rbp), %rax
	cmpq	-56(%rbp), %rax
	jb	.L23
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	generate_2d_denominator_table, .-generate_2d_denominator_table
	.globl	c_compute_mean_table_2d_shuffled
	.type	c_compute_mean_table_2d_shuffled, @function
c_compute_mean_table_2d_shuffled:
.LFB3:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$96, %rsp
	movq	%rdi, -56(%rbp)
	movq	%rsi, -64(%rbp)
	movq	%rdx, -72(%rbp)
	movq	%rcx, -80(%rbp)
	movq	%r8, -88(%rbp)
	movq	-64(%rbp), %rdx
	movq	-64(%rbp), %rcx
	movq	-88(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	get_row_ptrs
	movq	%rax, -32(%rbp)
	movq	-88(%rbp), %rdi
	movq	-80(%rbp), %rcx
	movq	-72(%rbp), %rdx
	movq	-64(%rbp), %rsi
	movq	-56(%rbp), %rax
	movq	%rdi, %r8
	movq	%rax, %rdi
	call	c_compute_sum_table_2d_shuffled
	movl	$0, %eax
	movq	%rax, -8(%rbp)
	movq	-72(%rbp), %rax
	movq	%rax, -16(%rbp)
	jmp	.L26
.L31:
	movq	-72(%rbp), %rax
	movq	-16(%rbp), %rdx
	subq	%rax, %rdx
	movq	%rdx, %rax
	addq	$1, %rax
	testq	%rax, %rax
	js	.L27
	cvtsi2sdq	%rax, %xmm0
	jmp	.L28
.L27:
	movq	%rax, %rdx
	shrq	%rdx
	andl	$1, %eax
	orq	%rax, %rdx
	cvtsi2sdq	%rdx, %xmm0
	addsd	%xmm0, %xmm0
.L28:
	movsd	-8(%rbp), %xmm1
	addsd	%xmm1, %xmm0
	movsd	%xmm0, -8(%rbp)
	movq	$0, -24(%rbp)
	jmp	.L29
.L30:
	movq	-16(%rbp), %rax
	movq	-24(%rbp), %rdx
	addq	%rdx, %rax
	movq	%rax, -40(%rbp)
	movq	-24(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-32(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-40(%rbp), %rdx
	salq	$3, %rdx
	addq	%rdx, %rax
	movq	-24(%rbp), %rdx
	leaq	0(,%rdx,8), %rcx
	movq	-32(%rbp), %rdx
	addq	%rcx, %rdx
	movq	(%rdx), %rdx
	movq	-40(%rbp), %rcx
	salq	$3, %rcx
	addq	%rcx, %rdx
	movsd	(%rdx), %xmm0
	divsd	-8(%rbp), %xmm0
	movsd	%xmm0, (%rax)
	addq	$1, -24(%rbp)
.L29:
	movq	-16(%rbp), %rax
	movq	-64(%rbp), %rdx
	subq	%rax, %rdx
	movq	%rdx, %rax
	cmpq	-24(%rbp), %rax
	ja	.L30
	addq	$1, -16(%rbp)
.L26:
	movq	-16(%rbp), %rax
	cmpq	-80(%rbp), %rax
	jb	.L31
	movq	-32(%rbp), %rax
	movq	%rax, %rdi
	call	free
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	c_compute_mean_table_2d_shuffled, .-c_compute_mean_table_2d_shuffled
	.globl	c_compute_sum_table_1d_shuffled
	.type	c_compute_sum_table_1d_shuffled, @function
c_compute_sum_table_1d_shuffled:
.LFB4:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	pushq	%rbx
	subq	$104, %rsp
	.cfi_offset 3, -24
	movq	%rdi, -88(%rbp)
	movq	%rsi, -96(%rbp)
	movq	%rdx, -104(%rbp)
	movq	%rcx, -112(%rbp)
	movq	%rsp, %rax
	movq	%rax, %rbx
	movq	-96(%rbp), %rax
	movq	%rax, %rdx
	subq	$1, %rdx
	movq	%rdx, -56(%rbp)
	movq	%rax, %r10
	movl	$0, %r11d
	movq	%rax, %r8
	movl	$0, %r9d
	salq	$3, %rax
	leaq	7(%rax), %rdx
	movl	$16, %eax
	subq	$1, %rax
	addq	%rdx, %rax
	movl	$16, %esi
	movl	$0, %edx
	divq	%rsi
	imulq	$16, %rax, %rax
	subq	%rax, %rsp
	movq	%rsp, %rax
	addq	$7, %rax
	shrq	$3, %rax
	salq	$3, %rax
	movq	%rax, -64(%rbp)
	movq	$0, -48(%rbp)
	jmp	.L34
.L35:
	movq	-64(%rbp), %rax
	movq	-48(%rbp), %rdx
	movq	-48(%rbp), %rcx
	movq	%rcx, (%rax,%rdx,8)
	addq	$1, -48(%rbp)
.L34:
	movq	-48(%rbp), %rax
	cmpq	-96(%rbp), %rax
	jb	.L35
	movq	-64(%rbp), %rax
	movq	-96(%rbp), %rdx
	movq	%rdx, %rsi
	movq	%rax, %rdi
	call	shuffle_array_st
	movq	-96(%rbp), %rdx
	movq	-96(%rbp), %rcx
	movq	-112(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	get_row_ptrs
	movq	%rax, -72(%rbp)
	movq	$0, -32(%rbp)
	jmp	.L36
.L41:
	movq	$0, -24(%rbp)
	jmp	.L37
.L40:
	movl	$0, %eax
	movq	%rax, -40(%rbp)
	movq	-32(%rbp), %rax
	movq	-24(%rbp), %rdx
	addq	%rdx, %rax
	movq	%rax, -80(%rbp)
	cmpq	$0, -32(%rbp)
	jne	.L38
	movq	-64(%rbp), %rax
	movq	-24(%rbp), %rdx
	movq	(%rax,%rdx,8), %rax
	leaq	0(,%rax,8), %rdx
	movq	-88(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	%rax, -40(%rbp)
	jmp	.L39
.L38:
	movq	-24(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-72(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-80(%rbp), %rdx
	salq	$3, %rdx
	subq	$8, %rdx
	addq	%rdx, %rax
	movsd	(%rax), %xmm0
	movsd	-40(%rbp), %xmm1
	addsd	%xmm1, %xmm0
	movsd	%xmm0, -40(%rbp)
	movq	-64(%rbp), %rax
	movq	-80(%rbp), %rdx
	movq	(%rax,%rdx,8), %rax
	leaq	0(,%rax,8), %rdx
	movq	-88(%rbp), %rax
	addq	%rdx, %rax
	movsd	(%rax), %xmm0
	movsd	-40(%rbp), %xmm1
	addsd	%xmm1, %xmm0
	movsd	%xmm0, -40(%rbp)
.L39:
	movq	-24(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-72(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-80(%rbp), %rdx
	salq	$3, %rdx
	addq	%rax, %rdx
	movq	-40(%rbp), %rax
	movq	%rax, (%rdx)
	addq	$1, -24(%rbp)
.L37:
	movq	-32(%rbp), %rax
	movq	-96(%rbp), %rdx
	subq	%rax, %rdx
	movq	%rdx, %rax
	cmpq	-24(%rbp), %rax
	ja	.L40
	addq	$1, -32(%rbp)
.L36:
	movq	-32(%rbp), %rax
	cmpq	-104(%rbp), %rax
	jb	.L41
	movq	-72(%rbp), %rax
	movq	%rax, %rdi
	call	free
	nop
	movq	%rbx, %rsp
	movq	-8(%rbp), %rbx
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	c_compute_sum_table_1d_shuffled, .-c_compute_sum_table_1d_shuffled
	.globl	c_compute_mean_table_1d_shuffled
	.type	c_compute_mean_table_1d_shuffled, @function
c_compute_mean_table_1d_shuffled:
.LFB5:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$64, %rsp
	movq	%rdi, -40(%rbp)
	movq	%rsi, -48(%rbp)
	movq	%rdx, -56(%rbp)
	movq	%rcx, -64(%rbp)
	movq	-48(%rbp), %rdx
	movq	-48(%rbp), %rcx
	movq	-64(%rbp), %rax
	movq	%rcx, %rsi
	movq	%rax, %rdi
	call	get_row_ptrs
	movq	%rax, -24(%rbp)
	movq	-64(%rbp), %rcx
	movq	-56(%rbp), %rdx
	movq	-48(%rbp), %rsi
	movq	-40(%rbp), %rax
	movq	%rax, %rdi
	call	c_compute_sum_table_1d_shuffled
	movq	$0, -8(%rbp)
	jmp	.L44
.L49:
	movq	$0, -16(%rbp)
	jmp	.L45
.L48:
	movq	-8(%rbp), %rax
	movq	-16(%rbp), %rdx
	addq	%rdx, %rax
	movq	%rax, -32(%rbp)
	movq	-16(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-32(%rbp), %rdx
	salq	$3, %rdx
	leaq	(%rax,%rdx), %rcx
	movq	-16(%rbp), %rax
	leaq	0(,%rax,8), %rdx
	movq	-24(%rbp), %rax
	addq	%rdx, %rax
	movq	(%rax), %rax
	movq	-32(%rbp), %rdx
	salq	$3, %rdx
	addq	%rdx, %rax
	movsd	(%rax), %xmm1
	movq	-8(%rbp), %rax
	addq	$1, %rax
	testq	%rax, %rax
	js	.L46
	cvtsi2sdq	%rax, %xmm0
	jmp	.L47
.L46:
	movq	%rax, %rdx
	shrq	%rdx
	andl	$1, %eax
	orq	%rax, %rdx
	cvtsi2sdq	%rdx, %xmm0
	addsd	%xmm0, %xmm0
.L47:
	divsd	%xmm0, %xmm1
	movapd	%xmm1, %xmm0
	movsd	%xmm0, (%rcx)
	addq	$1, -16(%rbp)
.L45:
	movq	-8(%rbp), %rax
	movq	-48(%rbp), %rdx
	subq	%rax, %rdx
	movq	%rdx, %rax
	cmpq	-16(%rbp), %rax
	ja	.L48
	addq	$1, -8(%rbp)
.L44:
	movq	-8(%rbp), %rax
	cmpq	-56(%rbp), %rax
	jb	.L49
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	call	free
	nop
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	c_compute_mean_table_1d_shuffled, .-c_compute_mean_table_1d_shuffled
	.ident	"GCC: (GNU) 4.8.5 20150623 (Red Hat 4.8.5-16)"
	.section	.note.GNU-stack,"",@progbits
