interface StatBarProps {
  label: string;
  value: number;
  max?: number;
  color?: "success" | "info" | "warning" | "destructive" | "muted";
  showValue?: boolean;
}

export const StatBar = ({ label, value, max = 100, color = "success", showValue = false }: StatBarProps) => {
  const percentage = max > 1 ? (value / max) * 100 : value;
  
  const colorClasses = {
    success: "bg-success",
    info: "bg-info",
    warning: "bg-warning",
    destructive: "bg-destructive",
    muted: "bg-muted-foreground",
  };

  return (
    <div className="space-y-1">
      {label && (
        <div className="flex justify-between text-xs">
          <span className="text-muted-foreground">{label}</span>
          {showValue && <span className={`font-semibold text-${color}`}>{value.toFixed(2)}</span>}
          {!showValue && <span className={`font-semibold text-${color}`}>{value}%</span>}
        </div>
      )}
      <div className="stat-bar">
        <div
          className={`stat-bar-fill ${colorClasses[color]}`}
          style={{ width: `${Math.min(percentage, 100)}%` }}
        />
      </div>
    </div>
  );
};
