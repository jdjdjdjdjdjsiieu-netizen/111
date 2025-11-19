import { useState } from "react";
import { trpc } from "@/lib/trpc";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Checkbox } from "@/components/ui/checkbox";
import { Textarea } from "@/components/ui/textarea";
import { Upload, Send, Plus, Trash2, Loader2 } from "lucide-react";
import { useAuth } from "@/_core/hooks/useAuth";
import { toast } from "sonner";

interface ContactForCampaign {
  id: string;
  name: string;
  phone?: string;
  telegramId?: string;
  selected: boolean;
}

export default function CampaignManager() {
  const { user, isAuthenticated } = useAuth();
  const [contacts, setContacts] = useState<ContactForCampaign[]>([]);
  const [campaignMessage, setCampaignMessage] = useState("");
  const [campaignName, setCampaignName] = useState("");
  const [newContactName, setNewContactName] = useState("");
  const [newContactPhone, setNewContactPhone] = useState("");
  const [newContactTgId, setNewContactTgId] = useState("");
  const [isSending, setIsSending] = useState(false);

  // Fetch campaigns
  const { data: campaigns } = trpc.campaigns.list.useQuery(undefined, {
    enabled: isAuthenticated,
  });

  // Create campaign mutation
  const createCampaignMutation = trpc.campaigns.create.useMutation({
    onSuccess: () => {
      toast.success("Кампания создана");
      setCampaignName("");
      setCampaignMessage("");
      setContacts([]);
    },
    onError: (error) => {
      toast.error(`Ошибка: ${error.message}`);
    },
  });

  const handleAddContact = () => {
    if (!newContactName.trim()) {
      toast.error("Введите имя контакта");
      return;
    }

    const newContact: ContactForCampaign = {
      id: `contact_${Date.now()}`,
      name: newContactName,
      phone: newContactPhone || undefined,
      telegramId: newContactTgId || undefined,
      selected: true,
    };

    setContacts([...contacts, newContact]);
    setNewContactName("");
    setNewContactPhone("");
    setNewContactTgId("");
    toast.success("Контакт добавлен");
  };

  const handleRemoveContact = (id: string) => {
    setContacts(contacts.filter((c) => c.id !== id));
  };

  const handleToggleContact = (id: string) => {
    setContacts(
      contacts.map((c) => (c.id === id ? { ...c, selected: !c.selected } : c))
    );
  };

  const handleSelectAll = () => {
    setContacts(contacts.map((c) => ({ ...c, selected: true })));
  };

  const handleDeselectAll = () => {
    setContacts(contacts.map((c) => ({ ...c, selected: false })));
  };

  const handleUploadFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (event) => {
      try {
        const content = event.target?.result as string;
        const lines = content.split("\n").filter((line) => line.trim());

        const newContacts: ContactForCampaign[] = lines.map((line, idx) => {
          const [name, phone, tgId] = line.split(",").map((s) => s.trim());
          return {
            id: `contact_${Date.now()}_${idx}`,
            name: name || "Контакт",
            phone: phone || undefined,
            telegramId: tgId || undefined,
            selected: true,
          };
        });

        setContacts([...contacts, ...newContacts]);
        toast.success(`Загружено ${newContacts.length} контактов`);
      } catch (error) {
        toast.error("Ошибка при загрузке файла");
      }
    };
    reader.readAsText(file);
  };

  const selectedCount = contacts.filter((c) => c.selected).length;

  const handleSendCampaign = async () => {
    if (!campaignName.trim()) {
      toast.error("Введите название кампании");
      return;
    }

    if (!campaignMessage.trim()) {
      toast.error("Введите текст сообщения");
      return;
    }

    if (selectedCount === 0) {
      toast.error("Выберите хотя бы один контакт");
      return;
    }

    setIsSending(true);

    try {
      await createCampaignMutation.mutateAsync({
        name: campaignName,
        message: campaignMessage,
        totalContacts: selectedCount,
      });
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="space-y-6 p-6 max-w-6xl mx-auto">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-foreground mb-2">Менеджер Рассылок</h1>
        <p className="text-muted-foreground">
          Создавайте и управляйте кампаниями рассылок для ваших контактов
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Campaign Settings */}
        <div className="lg:col-span-2 space-y-6">
          {/* Campaign Info */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Информация о кампании</h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Название кампании</label>
                <Input
                  placeholder="Например: Рассылка по Альфе"
                  value={campaignName}
                  onChange={(e) => setCampaignName(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">Текст сообщения</label>
                <Textarea
                  placeholder="Введите текст сообщения для рассылки..."
                  value={campaignMessage}
                  onChange={(e) => setCampaignMessage(e.target.value)}
                  rows={6}
                  className="resize-none"
                />
              </div>
            </div>
          </Card>

          {/* Add Contact */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Добавить контакт</h2>
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <Input
                  placeholder="Имя контакта"
                  value={newContactName}
                  onChange={(e) => setNewContactName(e.target.value)}
                />
                <Input
                  placeholder="Номер телефона (опционально)"
                  value={newContactPhone}
                  onChange={(e) => setNewContactPhone(e.target.value)}
                />
                <Input
                  placeholder="Telegram ID (опционально)"
                  value={newContactTgId}
                  onChange={(e) => setNewContactTgId(e.target.value)}
                />
              </div>
              <Button onClick={handleAddContact} className="w-full">
                <Plus className="w-4 h-4 mr-2" />
                Добавить контакт
              </Button>
            </div>
          </Card>

          {/* Upload File */}
          <Card className="p-6">
            <h2 className="text-xl font-semibold mb-4">Загрузить контакты из файла</h2>
            <div className="border-2 border-dashed border-border rounded-lg p-6 text-center">
              <Upload className="w-8 h-8 mx-auto mb-2 text-muted-foreground" />
              <p className="text-sm text-muted-foreground mb-4">
                Загрузите CSV или TXT файл (формат: Имя, Телефон, Telegram ID)
              </p>
              <label>
                <input
                  type="file"
                  accept=".csv,.txt"
                  onChange={handleUploadFile}
                  className="hidden"
                />
                <Button variant="outline" className="cursor-pointer">
                  Выбрать файл
                </Button>
              </label>
            </div>
          </Card>
        </div>

        {/* Right: Contacts List & Stats */}
        <div className="space-y-6">
          {/* Stats */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Статистика</h3>
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Всего контактов:</span>
                <span className="font-semibold">{contacts.length}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Выбрано:</span>
                <span className="font-semibold text-blue-600">{selectedCount}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Не выбрано:</span>
                <span className="font-semibold">{contacts.length - selectedCount}</span>
              </div>
            </div>
          </Card>

          {/* Actions */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Действия</h3>
            <div className="space-y-2">
              <Button onClick={handleSelectAll} variant="outline" className="w-full">
                Выбрать все
              </Button>
              <Button onClick={handleDeselectAll} variant="outline" className="w-full">
                Отменить выбор
              </Button>
              <Button
                onClick={handleSendCampaign}
                disabled={isSending || selectedCount === 0}
                className="w-full bg-blue-600 hover:bg-blue-700"
              >
                {isSending ? (
                  <>
                    <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                    Отправка...
                  </>
                ) : (
                  <>
                    <Send className="w-4 h-4 mr-2" />
                    Отправить рассылку
                  </>
                )}
              </Button>
            </div>
          </Card>

          {/* Contacts List */}
          <Card className="p-6">
            <h3 className="text-lg font-semibold mb-4">Контакты ({contacts.length})</h3>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {contacts.length === 0 ? (
                <p className="text-sm text-muted-foreground text-center py-4">
                  Нет контактов
                </p>
              ) : (
                contacts.map((contact) => (
                  <div
                    key={contact.id}
                    className="flex items-center justify-between p-3 rounded-lg border border-border hover:bg-gray-50"
                  >
                    <div className="flex items-center gap-3 flex-1">
                      <Checkbox
                        checked={contact.selected}
                        onCheckedChange={() => handleToggleContact(contact.id)}
                      />
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-sm truncate">{contact.name}</p>
                        {contact.phone && (
                          <p className="text-xs text-muted-foreground truncate">
                            {contact.phone}
                          </p>
                        )}
                      </div>
                    </div>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleRemoveContact(contact.id)}
                    >
                      <Trash2 className="w-4 h-4 text-red-500" />
                    </Button>
                  </div>
                ))
              )}
            </div>
          </Card>
        </div>
      </div>

      {/* Recent Campaigns */}
      {campaigns && campaigns.length > 0 && (
        <Card className="p-6">
          <h2 className="text-xl font-semibold mb-4">Последние кампании</h2>
          <div className="space-y-3">
            {campaigns.slice(0, 5).map((campaign) => (
              <div key={campaign.id} className="flex justify-between items-center p-3 border border-border rounded-lg">
                <div>
                  <p className="font-medium">{campaign.name}</p>
                  <p className="text-sm text-muted-foreground">
                    Отправлено: {campaign.sentCount} / {campaign.totalContacts}
                  </p>
                </div>
                <span className="text-xs px-2 py-1 bg-blue-100 text-blue-700 rounded">
                  {campaign.status}
                </span>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}
