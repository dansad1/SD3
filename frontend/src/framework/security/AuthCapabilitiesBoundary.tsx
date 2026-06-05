import { useContext } from "react"

import { AuthContext }
  from "@/framework/auth/AuthContext"

import { CapabilityBoundary }
  from "@/framework/security/CapabilityBoundary"

export function AuthCapabilitiesBoundary({
  children,
}: {
  children: React.ReactNode
}) {

  const auth =
    useContext(AuthContext)

  return (

    <CapabilityBoundary

      capabilities={
        auth?.me?.capabilities
      }

    >

      {children}

    </CapabilityBoundary>
  )
}