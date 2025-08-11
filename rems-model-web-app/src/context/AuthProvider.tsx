import {
  createContext,
  ReactNode,
  useContext,
  useState,
  useEffect,
} from "react";

type LoginType = {
  email: string;
  password: string;
  remember_me?: boolean | undefined;
};

interface AuthContextType {
  user: string | null;
  token: string | null;
  // login(data: LoginType): void;
  // logout(): void;
  setGoogleToken(token: string): void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<string | null>(
    localStorage.getItem("user") as string
  );
  const [token, setToken] = useState<string | null>(
    localStorage.getItem("authToken") as string
  );

  useEffect(() => {
    if (token) {
      localStorage.setItem("authToken", token);
    } else {
      localStorage.removeItem("authToken");
    }

    if (user) {
      localStorage.setItem("user", user);
    } else {
      localStorage.removeItem("user");
    }
  }, [token, user]);

  const setGoogleToken = (googleToken: string) => {
    setToken(googleToken);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token: token || "",
        setGoogleToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Custom Hook
export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used with an AuthProvider");
  }
  return context;
}
