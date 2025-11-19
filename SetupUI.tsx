/**
 * Setup UI - Веб-интерфейс для первоначальной настройки
 * Позволяет вводить API ключи через удобный веб-интерфейс
 */

import React, { useState, useEffect } from 'react';

interface EnvConfig {
  TELEGRAM_API_ID: string;
  TELEGRAM_API_HASH: string;
  TELEGRAM_PHONE_NUMBER: string;
  TELEGRAM_BOT_TOKEN?: string;
  GEMINI_API_KEY?: string;
  GROQ_API_KEY?: string;
  HUGGINGFACE_TOKEN?: string;
  DATABASE_URL: string;
}

interface ValidationResult {
  required: { [key: string]: boolean };
  optional: { [key: string]: boolean };
  has_ai_key: boolean;
  is_valid: boolean;
}

const SetupUI: React.FC = () => {
  const [config, setConfig] = useState<EnvConfig>({
    TELEGRAM_API_ID: '',
    TELEGRAM_API_HASH: '',
    TELEGRAM_PHONE_NUMBER: '',
    TELEGRAM_BOT_TOKEN: '',
    GEMINI_API_KEY: '',
    GROQ_API_KEY: '',
    HUGGINGFACE_TOKEN: '',
    DATABASE_URL: 'sqlite:///./alfa.db',
  });

  const [validation, setValidation] = useState<ValidationResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [saved, setSaved] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const [showGuides, setShowGuides] = useState(false);

  // Загрузить текущую конфигурацию
  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const response = await fetch('/api/config');
      if (response.ok) {
        const data = await response.json();
        setConfig(data);
      }
    } catch (error) {
      console.error('Failed to load config:', error);
    }
  };

  const validateConfig = async () => {
    try {
      const response = await fetch('/api/config/validate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      });
      const data = await response.json();
      setValidation(data);
      return data.is_valid;
    } catch (error) {
      console.error('Failed to validate config:', error);
      return false;
    }
  };

  const saveConfig = async () => {
    setLoading(true);
    setSaved(false);

    try {
      const isValid = await validateConfig();

      if (!isValid) {
        alert('Конфигурация невалидна! Проверьте обязательные поля.');
        setLoading(false);
        return;
      }

      const response = await fetch('/api/config/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      });

      if (response.ok) {
        setSaved(true);
        alert('✅ Конфигурация успешно сохранена!');
      } else {
        alert('❌ Ошибка при сохранении конфигурации');
      }
    } catch (error) {
      console.error('Failed to save config:', error);
      alert('❌ Ошибка при сохранении конфигурации');
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (key: keyof EnvConfig, value: string) => {
    setConfig({ ...config, [key]: value });
    setSaved(false);
  };

  const nextStep = () => {
    if (currentStep < 4) {
      setCurrentStep(currentStep + 1);
    }
  };

  const prevStep = () => {
    if (currentStep > 1) {
      setCurrentStep(currentStep - 1);
    }
  };

  return (
    <div style={styles.container}>
      {/* Header */}
      <div style={styles.header}>
        <h1 style={styles.title}>🚀 Alfa Campaign Manager</h1>
        <p style={styles.subtitle}>Мастер первоначальной настройки</p>
      </div>

      {/* Progress Bar */}
      <div style={styles.progressBar}>
        <div style={styles.progressStep}>
          <div style={currentStep >= 1 ? styles.stepActive : styles.stepInactive}>1</div>
          <span>Telegram API</span>
        </div>
        <div style={styles.progressLine} />
        <div style={styles.progressStep}>
          <div style={currentStep >= 2 ? styles.stepActive : styles.stepInactive}>2</div>
          <span>Bot Token</span>
        </div>
        <div style={styles.progressLine} />
        <div style={styles.progressStep}>
          <div style={currentStep >= 3 ? styles.stepActive : styles.stepInactive}>3</div>
          <span>AI APIs</span>
        </div>
        <div style={styles.progressLine} />
        <div style={styles.progressStep}>
          <div style={currentStep >= 4 ? styles.stepActive : styles.stepInactive}>4</div>
          <span>База данных</span>
        </div>
      </div>

      {/* Content */}
      <div style={styles.content}>
        {/* Step 1: Telegram API */}
        {currentStep === 1 && (
          <div style={styles.step}>
            <h2 style={styles.stepTitle}>1. Telegram API Credentials</h2>
            <p style={styles.stepDescription}>
              Получите API_ID и API_HASH на{' '}
              <a href="https://my.telegram.org" target="_blank" rel="noopener noreferrer">
                my.telegram.org
              </a>
            </p>

            <div style={styles.guideBox}>
              <h4>📚 Инструкция:</h4>
              <ol>
                <li>Войдите на https://my.telegram.org</li>
                <li>Перейдите в "API development tools"</li>
                <li>Создайте приложение</li>
                <li>Скопируйте API_ID и API_HASH</li>
              </ol>
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>
                TELEGRAM_API_ID <span style={styles.required}>*</span>
              </label>
              <input
                type="text"
                style={styles.input}
                value={config.TELEGRAM_API_ID}
                onChange={(e) => handleChange('TELEGRAM_API_ID', e.target.value)}
                placeholder="12345678"
              />
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>
                TELEGRAM_API_HASH <span style={styles.required}>*</span>
              </label>
              <input
                type="password"
                style={styles.input}
                value={config.TELEGRAM_API_HASH}
                onChange={(e) => handleChange('TELEGRAM_API_HASH', e.target.value)}
                placeholder="0123456789abcdef0123456789abcdef"
              />
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>
                TELEGRAM_PHONE_NUMBER <span style={styles.required}>*</span>
              </label>
              <input
                type="tel"
                style={styles.input}
                value={config.TELEGRAM_PHONE_NUMBER}
                onChange={(e) => handleChange('TELEGRAM_PHONE_NUMBER', e.target.value)}
                placeholder="+79991234567"
              />
            </div>
          </div>
        )}

        {/* Step 2: Bot Token */}
        {currentStep === 2 && (
          <div style={styles.step}>
            <h2 style={styles.stepTitle}>2. Telegram Bot Token (Опционально)</h2>
            <p style={styles.stepDescription}>
              Если у вас есть Telegram Bot Token, введите его. Это опционально.
            </p>

            <div style={styles.warningBox}>
              <strong>⚠️ Внимание:</strong> Бот может работать через User API (Telethon) без Bot Token
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>TELEGRAM_BOT_TOKEN</label>
              <input
                type="password"
                style={styles.input}
                value={config.TELEGRAM_BOT_TOKEN || ''}
                onChange={(e) => handleChange('TELEGRAM_BOT_TOKEN', e.target.value)}
                placeholder="1234567890:ABCdefGHIjklMNOpqrsTUVwxyz"
              />
            </div>
          </div>
        )}

        {/* Step 3: AI APIs */}
        {currentStep === 3 && (
          <div style={styles.step}>
            <h2 style={styles.stepTitle}>3. AI API Ключи</h2>
            <p style={styles.stepDescription}>
              Необходим хотя бы один AI API ключ для работы бота
            </p>

            <div style={styles.warningBox}>
              <strong>💡 Рекомендация:</strong> Настройте оба ключа (Gemini и Groq) для резервирования
            </div>

            {/* Gemini API */}
            <div style={styles.apiBox}>
              <h4>🟢 Google Gemini API (БЕСПЛАТНО)</h4>
              <p>
                60 запросов/мин •{' '}
                <a href="https://makersuite.google.com/app/apikey" target="_blank" rel="noopener noreferrer">
                  Получить ключ
                </a>
              </p>
              <input
                type="password"
                style={styles.input}
                value={config.GEMINI_API_KEY || ''}
                onChange={(e) => handleChange('GEMINI_API_KEY', e.target.value)}
                placeholder="AIzaSyD-9tSrke72PouQMnMX-a7eZSW0jkFMBWY"
              />
            </div>

            {/* Groq API */}
            <div style={styles.apiBox}>
              <h4>🟣 Groq API (БЕСПЛАТНО, очень быстро)</h4>
              <p>
                30 запросов/мин •{' '}
                <a href="https://console.groq.com" target="_blank" rel="noopener noreferrer">
                  Получить ключ
                </a>
              </p>
              <input
                type="password"
                style={styles.input}
                value={config.GROQ_API_KEY || ''}
                onChange={(e) => handleChange('GROQ_API_KEY', e.target.value)}
                placeholder="gsk_1234567890abcdefghijklmnopqrstuv"
              />
            </div>

            {/* Hugging Face */}
            <div style={styles.apiBox}>
              <h4>🟡 Hugging Face Token (Опционально)</h4>
              <p>
                <a href="https://huggingface.co/settings/tokens" target="_blank" rel="noopener noreferrer">
                  Получить токен
                </a>
              </p>
              <input
                type="password"
                style={styles.input}
                value={config.HUGGINGFACE_TOKEN || ''}
                onChange={(e) => handleChange('HUGGINGFACE_TOKEN', e.target.value)}
                placeholder="hf_1234567890abcdefghijklmnopqrstuv"
              />
            </div>
          </div>
        )}

        {/* Step 4: Database */}
        {currentStep === 4 && (
          <div style={styles.step}>
            <h2 style={styles.stepTitle}>4. База данных</h2>
            <p style={styles.stepDescription}>Настройка подключения к базе данных</p>

            <div style={styles.infoBox}>
              <strong>ℹ️ По умолчанию:</strong> Используется SQLite (файловая БД, не требует настройки)
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>DATABASE_URL</label>
              <input
                type="text"
                style={styles.input}
                value={config.DATABASE_URL}
                onChange={(e) => handleChange('DATABASE_URL', e.target.value)}
                placeholder="sqlite:///./alfa.db"
              />
              <small style={styles.hint}>
                Для PostgreSQL: postgresql://user:password@localhost/alfa_db
              </small>
            </div>

            {/* Validation Status */}
            {validation && (
              <div style={styles.validationBox}>
                <h4>📊 Статус конфигурации:</h4>
                <div>
                  {validation.is_valid ? (
                    <div style={styles.successBox}>✅ Конфигурация валидна!</div>
                  ) : (
                    <div style={styles.errorBox}>❌ Конфигурация невалидна</div>
                  )}
                </div>
                {!validation.has_ai_key && (
                  <div style={styles.errorBox}>⚠️ Необходим хотя бы один AI API ключ</div>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Navigation */}
      <div style={styles.navigation}>
        <button
          style={currentStep === 1 ? styles.buttonDisabled : styles.buttonSecondary}
          onClick={prevStep}
          disabled={currentStep === 1}
        >
          ← Назад
        </button>

        {currentStep < 4 ? (
          <button style={styles.buttonPrimary} onClick={nextStep}>
            Далее →
          </button>
        ) : (
          <button
            style={loading ? styles.buttonDisabled : styles.buttonSuccess}
            onClick={saveConfig}
            disabled={loading}
          >
            {loading ? 'Сохранение...' : saved ? '✓ Сохранено' : '💾 Сохранить конфигурацию'}
          </button>
        )}
      </div>

      {/* Footer */}
      <div style={styles.footer}>
        <p>
          После сохранения конфигурации запустите: <code>python main.py</code>
        </p>
      </div>
    </div>
  );
};

// Styles
const styles: { [key: string]: React.CSSProperties } = {
  container: {
    maxWidth: '800px',
    margin: '0 auto',
    padding: '20px',
    fontFamily: 'Arial, sans-serif',
  },
  header: {
    textAlign: 'center',
    marginBottom: '30px',
  },
  title: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#2c3e50',
    margin: '0',
  },
  subtitle: {
    fontSize: '16px',
    color: '#7f8c8d',
    margin: '10px 0 0 0',
  },
  progressBar: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: '40px',
  },
  progressStep: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    gap: '8px',
  },
  stepActive: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    backgroundColor: '#3498db',
    color: 'white',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 'bold',
  },
  stepInactive: {
    width: '40px',
    height: '40px',
    borderRadius: '50%',
    backgroundColor: '#ecf0f1',
    color: '#95a5a6',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  progressLine: {
    flex: 1,
    height: '2px',
    backgroundColor: '#ecf0f1',
    margin: '0 10px',
  },
  content: {
    backgroundColor: 'white',
    borderRadius: '8px',
    padding: '30px',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
    minHeight: '400px',
  },
  step: {
    animation: 'fadeIn 0.3s',
  },
  stepTitle: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: '10px',
  },
  stepDescription: {
    fontSize: '14px',
    color: '#7f8c8d',
    marginBottom: '20px',
  },
  formGroup: {
    marginBottom: '20px',
  },
  label: {
    display: 'block',
    fontSize: '14px',
    fontWeight: 'bold',
    color: '#2c3e50',
    marginBottom: '8px',
  },
  required: {
    color: '#e74c3c',
  },
  input: {
    width: '100%',
    padding: '12px',
    fontSize: '14px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    boxSizing: 'border-box',
  },
  hint: {
    fontSize: '12px',
    color: '#95a5a6',
    marginTop: '5px',
    display: 'block',
  },
  guideBox: {
    backgroundColor: '#e8f4fd',
    border: '1px solid #3498db',
    borderRadius: '4px',
    padding: '15px',
    marginBottom: '20px',
  },
  infoBox: {
    backgroundColor: '#e8f4fd',
    border: '1px solid #3498db',
    borderRadius: '4px',
    padding: '15px',
    marginBottom: '20px',
  },
  warningBox: {
    backgroundColor: '#fff3cd',
    border: '1px solid #f39c12',
    borderRadius: '4px',
    padding: '15px',
    marginBottom: '20px',
  },
  apiBox: {
    border: '1px solid #ddd',
    borderRadius: '4px',
    padding: '15px',
    marginBottom: '15px',
  },
  validationBox: {
    marginTop: '20px',
    padding: '15px',
    border: '1px solid #ddd',
    borderRadius: '4px',
  },
  successBox: {
    backgroundColor: '#d4edda',
    color: '#155724',
    padding: '10px',
    borderRadius: '4px',
    marginTop: '10px',
  },
  errorBox: {
    backgroundColor: '#f8d7da',
    color: '#721c24',
    padding: '10px',
    borderRadius: '4px',
    marginTop: '10px',
  },
  navigation: {
    display: 'flex',
    justifyContent: 'space-between',
    marginTop: '30px',
  },
  buttonPrimary: {
    padding: '12px 30px',
    fontSize: '16px',
    fontWeight: 'bold',
    color: 'white',
    backgroundColor: '#3498db',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  buttonSecondary: {
    padding: '12px 30px',
    fontSize: '16px',
    fontWeight: 'bold',
    color: '#3498db',
    backgroundColor: 'white',
    border: '2px solid #3498db',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  buttonSuccess: {
    padding: '12px 30px',
    fontSize: '16px',
    fontWeight: 'bold',
    color: 'white',
    backgroundColor: '#27ae60',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  buttonDisabled: {
    padding: '12px 30px',
    fontSize: '16px',
    fontWeight: 'bold',
    color: '#95a5a6',
    backgroundColor: '#ecf0f1',
    border: 'none',
    borderRadius: '4px',
    cursor: 'not-allowed',
  },
  footer: {
    textAlign: 'center',
    marginTop: '30px',
    color: '#7f8c8d',
    fontSize: '14px',
  },
};

export default SetupUI;
