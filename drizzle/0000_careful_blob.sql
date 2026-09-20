CREATE TABLE `ai_insights` (
	`id` text NOT NULL,
	`workspace` text NOT NULL,
	`data` text NOT NULL,
	PRIMARY KEY(`workspace`, `id`)
);
--> statement-breakpoint
CREATE TABLE `analytics` (
	`id` text NOT NULL,
	`workspace` text NOT NULL,
	`data` text NOT NULL,
	PRIMARY KEY(`workspace`, `id`)
);
--> statement-breakpoint
CREATE TABLE `documents` (
	`id` text NOT NULL,
	`workspace` text NOT NULL,
	`data` text NOT NULL,
	PRIMARY KEY(`workspace`, `id`)
);
--> statement-breakpoint
CREATE TABLE `payments` (
	`id` text NOT NULL,
	`workspace` text NOT NULL,
	`data` text NOT NULL,
	PRIMARY KEY(`workspace`, `id`)
);
--> statement-breakpoint
CREATE TABLE `pricing` (
	`id` text NOT NULL,
	`workspace` text NOT NULL,
	`data` text NOT NULL,
	PRIMARY KEY(`workspace`, `id`)
);
--> statement-breakpoint
CREATE TABLE `print_jobs` (
	`id` text NOT NULL,
	`workspace` text NOT NULL,
	`data` text NOT NULL,
	PRIMARY KEY(`workspace`, `id`)
);
--> statement-breakpoint
CREATE TABLE `printer_status` (
	`id` text NOT NULL,
	`workspace` text NOT NULL,
	`data` text NOT NULL,
	PRIMARY KEY(`workspace`, `id`)
);
--> statement-breakpoint
CREATE TABLE `printers` (
	`id` text NOT NULL,
	`workspace` text NOT NULL,
	`data` text NOT NULL,
	PRIMARY KEY(`workspace`, `id`)
);
--> statement-breakpoint
CREATE TABLE `rate_limits` (
	`workspace` text PRIMARY KEY NOT NULL,
	`window` integer NOT NULL,
	`count` integer NOT NULL
);
--> statement-breakpoint
CREATE TABLE `resource_usage` (
	`id` text NOT NULL,
	`workspace` text NOT NULL,
	`data` text NOT NULL,
	PRIMARY KEY(`workspace`, `id`)
);
--> statement-breakpoint
CREATE TABLE `users` (
	`id` text NOT NULL,
	`workspace` text NOT NULL,
	`data` text NOT NULL,
	PRIMARY KEY(`workspace`, `id`)
);
