import { Link } from "@tanstack/react-router"
import { HeartPulse } from "lucide-react"

import { cn } from "@/lib/utils"

interface LogoProps {
  variant?: "full" | "icon" | "responsive"
  className?: string
  asLink?: boolean
}

function LogoMark({ className }: { className?: string }) {
  return (
    <span
      className={cn(
        "flex size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground",
        className,
      )}
    >
      <HeartPulse className="size-4" />
    </span>
  )
}

export function Logo({
  variant = "full",
  className,
  asLink = true,
}: LogoProps) {
  const content =
    variant === "icon" ? (
      <LogoMark className={className} />
    ) : variant === "responsive" ? (
      <span className="flex items-center gap-2">
        <LogoMark className="group-data-[collapsible=icon]:size-8" />
        <span
          className={cn(
            "font-semibold tracking-tight group-data-[collapsible=icon]:hidden",
            className,
          )}
        >
          HealSync AI
        </span>
      </span>
    ) : (
      <span className={cn("flex items-center gap-2 font-semibold", className)}>
        <LogoMark />
        HealSync AI
      </span>
    )

  if (!asLink) {
    return content
  }

  return <Link to="/">{content}</Link>
}
