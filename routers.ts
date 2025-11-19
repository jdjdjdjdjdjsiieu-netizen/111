import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, router, protectedProcedure } from "./_core/trpc";
import { getContactsByUserId, createContact, getChatsByUserId, createChat, getMessagesByContactId, createMessage, getCampaignsByUserId, createCampaign } from "./db";
import { telethonRouter } from "./routers/telethon_router";

export const appRouter = router({
  system: systemRouter,
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return {
        success: true,
      } as const;
    }),
  }),

  contacts: router({
    list: protectedProcedure.query(({ ctx }) => getContactsByUserId(ctx.user.id)),
    create: protectedProcedure
      .input((val: any) => val)
      .mutation(({ ctx, input }) => 
        createContact({
          userId: ctx.user.id,
          ...input,
        })
      ),
  }),

  chats: router({
    list: protectedProcedure.query(({ ctx }) => getChatsByUserId(ctx.user.id)),
    create: protectedProcedure
      .input((val: any) => val)
      .mutation(({ ctx, input }) =>
        createChat({
          userId: ctx.user.id,
          ...input,
        })
      ),
  }),

  messages: router({
    getByContact: protectedProcedure
      .input((val: any) => val)
      .query(({ ctx, input }) => getMessagesByContactId(ctx.user.id, input.contactId)),
    create: protectedProcedure
      .input((val: any) => val)
      .mutation(({ ctx, input }) =>
        createMessage({
          userId: ctx.user.id,
          ...input,
        })
      ),
  }),

  campaigns: router({
    list: protectedProcedure.query(({ ctx }) => getCampaignsByUserId(ctx.user.id)),
    create: protectedProcedure
      .input((val: any) => val)
      .mutation(({ ctx, input }) =>
        createCampaign({
          userId: ctx.user.id,
          ...input,
        })
      ),
  }),

  telethon: telethonRouter,
});

export type AppRouter = typeof appRouter;
