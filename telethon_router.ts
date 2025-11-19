import { router, protectedProcedure } from "../_core/trpc";
import { TRPCError } from "@trpc/server";
import axios from "axios";

const PYTHON_API_URL = process.env.PYTHON_API_URL || "http://localhost:8000";

const pythonApi = axios.create({
  baseURL: PYTHON_API_URL,
  timeout: 30000,
});

export const telethonRouter = router({
  // Подключиться к Telegram
  connect: protectedProcedure.mutation(async ({ ctx }) => {
    try {
      const response = await pythonApi.post("/api/telethon/connect");
      return response.data;
    } catch (error: any) {
      throw new TRPCError({
        code: "INTERNAL_SERVER_ERROR",
        message: error.response?.data?.detail || "Ошибка подключения к Telegram",
      });
    }
  }),

  // Синхронизировать контакты
  syncContacts: protectedProcedure.mutation(async ({ ctx }) => {
    try {
      const response = await pythonApi.post("/api/telethon/sync-contacts");
      return response.data;
    } catch (error: any) {
      throw new TRPCError({
        code: "INTERNAL_SERVER_ERROR",
        message: error.response?.data?.detail || "Ошибка синхронизации контактов",
      });
    }
  }),

  // Получить группы и каналы
  getGroupsAndChannels: protectedProcedure.query(async ({ ctx }) => {
    try {
      const response = await pythonApi.post("/api/telethon/groups-channels");
      return response.data;
    } catch (error: any) {
      throw new TRPCError({
        code: "INTERNAL_SERVER_ERROR",
        message: error.response?.data?.detail || "Ошибка получения групп/каналов",
      });
    }
  }),

  // Получить контакты
  getContacts: protectedProcedure
    .input((val: any) => val)
    .query(async ({ ctx, input }) => {
      try {
        const response = await pythonApi.get("/api/contacts", {
          params: {
            skip: input?.skip || 0,
            limit: input?.limit || 100,
          },
        });
        return response.data;
      } catch (error: any) {
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: error.response?.data?.detail || "Ошибка получения контактов",
        });
      }
    }),

  // Создать контакт
  createContact: protectedProcedure
    .input((val: any) => val)
    .mutation(async ({ ctx, input }) => {
      try {
        const response = await pythonApi.post("/api/contacts", input);
        return response.data;
      } catch (error: any) {
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: error.response?.data?.detail || "Ошибка создания контакта",
        });
      }
    }),

  // Получить кампании
  getCampaigns: protectedProcedure
    .input((val: any) => val)
    .query(async ({ ctx, input }) => {
      try {
        const response = await pythonApi.get("/api/campaigns", {
          params: {
            skip: input?.skip || 0,
            limit: input?.limit || 50,
          },
        });
        return response.data;
      } catch (error: any) {
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: error.response?.data?.detail || "Ошибка получения кампаний",
        });
      }
    }),

  // Создать кампанию
  createCampaign: protectedProcedure
    .input((val: any) => val)
    .mutation(async ({ ctx, input }) => {
      try {
        const response = await pythonApi.post("/api/campaigns", input);
        return response.data;
      } catch (error: any) {
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: error.response?.data?.detail || "Ошибка создания кампании",
        });
      }
    }),

  // Отправить кампанию
  sendCampaign: protectedProcedure
    .input((val: any) => val)
    .mutation(async ({ ctx, input }) => {
      try {
        const response = await pythonApi.post(
          `/api/campaigns/${input.campaignId}/send`,
          { contact_ids: input.contactIds }
        );
        return response.data;
      } catch (error: any) {
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: error.response?.data?.detail || "Ошибка отправки кампании",
        });
      }
    }),

  // Получить сообщения
  getMessages: protectedProcedure
    .input((val: any) => val)
    .query(async ({ ctx, input }) => {
      try {
        const response = await pythonApi.get(`/api/messages/${input.contactId}`);
        return response.data;
      } catch (error: any) {
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: error.response?.data?.detail || "Ошибка получения сообщений",
        });
      }
    }),

  // Отправить сообщение
  sendMessage: protectedProcedure
    .input((val: any) => val)
    .mutation(async ({ ctx, input }) => {
      try {
        const response = await pythonApi.post("/api/messages", input);
        return response.data;
      } catch (error: any) {
        throw new TRPCError({
          code: "INTERNAL_SERVER_ERROR",
          message: error.response?.data?.detail || "Ошибка отправки сообщения",
        });
      }
    }),
});
