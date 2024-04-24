import { FC, ReactNode } from "react";


type Props = {
  children: ReactNode;
};

export const BasicLayout: FC<Props> = ({ children }) => {
  return (
    <div className="flex flex-col w-screen h-screen overflow-hidden">
      <div className="relative flex h-full overflow-y-auto bg-gray-100 grow">
        <div className="h-full overflow-y-auto text-gray-700 grow">
          {children}
        </div>
      </div>
    </div>
  );
};
