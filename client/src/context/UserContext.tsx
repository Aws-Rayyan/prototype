import axios, { type AxiosInstance } from "axios";
import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import type { User } from "../types";

const STORAGE_KEY = "gaia:userId";

export const MOCK_USERS: User[] = [
  {
    id: "alice",
    name: "Alice Johnson",
    role: "sales_manager",
  },
  {
    id: "bob",
    name: "Bob Smith",
    role: "hr_manager",
  },
  {
    id: "aws",
    name: "Aws Rayyan",
    role: "no_document_access",
  },
];

type Ctx = {
  user: User;
  setUserId: (id: string) => void;
  api: AxiosInstance;
};

const UserContext = createContext<Ctx | null>(null);

function loadInitialId(): string {
  if (typeof window === "undefined") return "alice";
  const stored = window.localStorage.getItem(STORAGE_KEY);
  if (stored && MOCK_USERS.some((u) => u.id === stored)) return stored;
  return "alice";
}

export function UserProvider({ children }: { children: ReactNode }) {
  const [userId, setUserIdState] = useState<string>(loadInitialId);

  const user = MOCK_USERS.find((u) => u.id === userId) ?? MOCK_USERS[0];

  const setUserId = useCallback((id: string) => {
    window.localStorage.setItem(STORAGE_KEY, id);
    setUserIdState(id);
  }, []);

  const api = useMemo(() => {
    const instance = axios.create({
      baseURL: "",
    });
    instance.interceptors.request.use((config) => {
      config.headers.set("X-User-Id", userId);
      return config;
    });
    return instance;
  }, [userId]);

  const value = useMemo(
    () => ({
      user,
      setUserId,
      api,
    }),
    [user, setUserId, api],
  );

  return (
    <UserContext.Provider value={value}>{children}</UserContext.Provider>
  );
}

export function useUserContext(): Ctx {
  const ctx = useContext(UserContext);
  if (!ctx) {
    throw new Error("UserProvider missing");
  }
  return ctx;
}
