import { int, mysqlEnum, mysqlTable, text, timestamp, varchar } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 * Extend this file with additional tables as your product grows.
 * Columns use camelCase to match both database fields and generated types.
 */
export const users = mysqlTable("users", {
  /**
   * Surrogate primary key. Auto-incremented numeric value managed by the database.
   * Use this for relations between tables.
   */
  id: int("id").autoincrement().primaryKey(),
  /** Manus OAuth identifier (openId) returned from the OAuth callback. Unique per user. */
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

// Contacts table
export const contacts = mysqlTable("contacts", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("user_id").notNull(),
  telegramId: varchar("telegram_id", { length: 64 }).notNull(),
  firstName: varchar("first_name", { length: 255 }),
  lastName: varchar("last_name", { length: 255 }),
  phone: varchar("phone", { length: 20 }),
  username: varchar("username", { length: 255 }),
  isBot: int("is_bot").default(0).notNull(),
  isActive: int("is_active").default(1).notNull(),
  lastMessageAt: timestamp("last_message_at"),
  addedAt: timestamp("added_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().onUpdateNow().notNull(),
});

// Groups and Channels table
export const chats = mysqlTable("chats", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("user_id").notNull(),
  telegramId: varchar("telegram_id", { length: 64 }).notNull(),
  title: varchar("title", { length: 255 }).notNull(),
  type: mysqlEnum("type", ["private", "group", "supergroup", "channel"]).notNull(),
  membersCount: int("members_count").default(0),
  description: text("description"),
  isParsed: int("is_parsed").default(0).notNull(),
  lastParsedAt: timestamp("last_parsed_at"),
  addedAt: timestamp("added_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().onUpdateNow().notNull(),
});

// Messages table
export const messages = mysqlTable("messages", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("user_id").notNull(),
  contactId: int("contact_id"),
  chatId: int("chat_id"),
  telegramMessageId: varchar("telegram_message_id", { length: 64 }),
  senderTelegramId: varchar("sender_telegram_id", { length: 64 }),
  senderName: varchar("sender_name", { length: 255 }),
  text: text("text"),
  direction: mysqlEnum("direction", ["incoming", "outgoing"]).notNull(),
  status: mysqlEnum("status", ["sent", "delivered", "read", "failed"]).default("sent"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Campaign tracking table
export const campaigns = mysqlTable("campaigns", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("user_id").notNull(),
  name: varchar("name", { length: 255 }).notNull(),
  message: text("message").notNull(),
  totalContacts: int("total_contacts").default(0),
  sentCount: int("sent_count").default(0),
  deliveredCount: int("delivered_count").default(0),
  readCount: int("read_count").default(0),
  responseCount: int("response_count").default(0),
  status: mysqlEnum("status", ["draft", "scheduled", "running", "completed", "paused"]).default("draft"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().onUpdateNow().notNull(),
});

export type Contact = typeof contacts.$inferSelect;
export type InsertContact = typeof contacts.$inferInsert;

export type Chat = typeof chats.$inferSelect;
export type InsertChat = typeof chats.$inferInsert;

export type Message = typeof messages.$inferSelect;
export type InsertMessage = typeof messages.$inferInsert;

export type Campaign = typeof campaigns.$inferSelect;
export type InsertCampaign = typeof campaigns.$inferInsert;