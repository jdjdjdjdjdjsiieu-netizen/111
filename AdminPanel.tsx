import { useState } from "react";
import { trpc } from "@/lib/trpc";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Loader2, Send, Search, Plus } from "lucide-react";
import { useAuth } from "@/_core/hooks/useAuth";

export default function AdminPanel() {
  const { user, isAuthenticated } = useAuth();
  const [selectedContact, setSelectedContact] = useState<number | null>(null);
  const [messageText, setMessageText] = useState("");
  const [searchQuery, setSearchQuery] = useState("");

  // Fetch contacts
  const { data: contacts, isLoading: contactsLoading } = trpc.contacts.list.useQuery(undefined, {
    enabled: isAuthenticated,
  });

  // Fetch chats
  const { data: chats, isLoading: chatsLoading } = trpc.chats.list.useQuery(undefined, {
    enabled: isAuthenticated,
  });

  // Fetch messages for selected contact
  const { data: messages, isLoading: messagesLoading } = trpc.messages.getByContact.useQuery(
    { contactId: selectedContact || 0 },
    { enabled: isAuthenticated && selectedContact !== null }
  );

  // Send message mutation
  const sendMessageMutation = trpc.messages.create.useMutation({
    onSuccess: () => {
      setMessageText("");
    },
  });

  const handleSendMessage = () => {
    if (!messageText.trim() || !selectedContact) return;

    sendMessageMutation.mutate({
      contactId: selectedContact,
      text: messageText,
      direction: "outgoing",
      senderTelegramId: user?.id?.toString() || "",
      senderName: user?.name || "You",
    });
  };

  const filteredContacts = contacts?.filter((c) =>
    `${c.firstName} ${c.lastName}`.toLowerCase().includes(searchQuery.toLowerCase())
  ) || [];

  return (
    <div className="flex h-screen bg-background">
      {/* Left Sidebar - Contacts/Chats */}
      <div className="w-80 border-r border-border flex flex-col bg-white">
        {/* Header */}
        <div className="p-4 border-b border-border">
          <h1 className="text-2xl font-bold text-foreground mb-4">Альфа Админка</h1>
          <div className="relative">
            <Search className="absolute left-3 top-3 w-4 h-4 text-muted-foreground" />
            <Input
              placeholder="Поиск контактов..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* Contacts List */}
        <div className="flex-1 overflow-y-auto">
          {contactsLoading ? (
            <div className="flex items-center justify-center h-full">
              <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
            </div>
          ) : filteredContacts.length === 0 ? (
            <div className="p-4 text-center text-muted-foreground">
              Нет контактов
            </div>
          ) : (
            filteredContacts.map((contact) => (
              <div
                key={contact.id}
                onClick={() => setSelectedContact(contact.id)}
                className={`p-4 border-b border-border cursor-pointer transition-colors ${
                  selectedContact === contact.id
                    ? "bg-blue-50 border-l-4 border-l-blue-500"
                    : "hover:bg-gray-50"
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-foreground">
                      {contact.firstName} {contact.lastName}
                    </h3>
                    <p className="text-sm text-muted-foreground">{contact.phone}</p>
                  </div>
                  {contact.isActive ? (
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  ) : (
                    <div className="w-3 h-3 bg-gray-300 rounded-full"></div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>

        {/* Add Contact Button */}
        <div className="p-4 border-t border-border">
          <Button className="w-full" variant="default">
            <Plus className="w-4 h-4 mr-2" />
            Добавить контакт
          </Button>
        </div>
      </div>

      {/* Right Side - Chat View */}
      <div className="flex-1 flex flex-col bg-white">
        {selectedContact ? (
          <>
            {/* Chat Header */}
            <div className="p-4 border-b border-border bg-white">
              <h2 className="text-xl font-semibold text-foreground">
                {contacts?.find((c) => c.id === selectedContact)?.firstName}{" "}
                {contacts?.find((c) => c.id === selectedContact)?.lastName}
              </h2>
              <p className="text-sm text-muted-foreground">
                {contacts?.find((c) => c.id === selectedContact)?.phone}
              </p>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
              {messagesLoading ? (
                <div className="flex items-center justify-center h-full">
                  <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
                </div>
              ) : messages && messages.length > 0 ? (
                <div className="space-y-4">
                  {messages.map((msg) => (
                    <div
                      key={msg.id}
                      className={`flex ${msg.direction === "outgoing" ? "justify-end" : "justify-start"}`}
                    >
                      <div
                        className={`max-w-xs px-4 py-2 rounded-lg ${
                          msg.direction === "outgoing"
                            ? "bg-blue-500 text-white"
                            : "bg-white text-foreground border border-border"
                        }`}
                      >
                        <p>{msg.text}</p>
                        <p className="text-xs mt-1 opacity-70">
                          {new Date(msg.createdAt).toLocaleTimeString()}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex items-center justify-center h-full text-muted-foreground">
                  Нет сообщений
                </div>
              )}
            </div>

            {/* Message Input */}
            <div className="p-4 border-t border-border bg-white">
              <div className="flex gap-2">
                <Input
                  placeholder="Введите сообщение..."
                  value={messageText}
                  onChange={(e) => setMessageText(e.target.value)}
                  onKeyPress={(e) => {
                    if (e.key === "Enter") handleSendMessage();
                  }}
                  className="flex-1"
                />
                <Button
                  onClick={handleSendMessage}
                  disabled={!messageText.trim() || sendMessageMutation.isPending}
                  className="bg-blue-500 hover:bg-blue-600"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
          </>
        ) : (
          <div className="flex items-center justify-center h-full text-muted-foreground">
            Выберите контакт для начала общения
          </div>
        )}
      </div>
    </div>
  );
}
