import SwiftUI

/// Central place for category colour-coding, mirroring the original
/// PharmaPulse HTML CSS classes (cat-approval, cat-crl, …).
enum Theme {
    /// Brand accent used across the app.
    static let accent = Color(hex: "1E3A8A")          // deep pharma blue

    /// Map a `catClass` string from the feed to its colour.
    static func color(for catClass: String) -> Color {
        switch catClass {
        case "cat-approval":   return Color(hex: "16A34A") // green  – approvals
        case "cat-regulatory": return Color(hex: "2563EB") // blue   – FDA regulatory
        case "cat-phase3":     return Color(hex: "7C3AED") // purple – Phase III
        case "cat-biosimilar": return Color(hex: "0D9488") // teal   – biosimilars
        case "cat-crl":        return Color(hex: "DC2626") // red    – CRLs
        case "cat-deals":      return Color(hex: "EA580C") // orange – M&A / deals
        case "cat-outlook":    return Color(hex: "4F46E5") // indigo – outlook
        case "cat-eu":         return Color(hex: "0891B2") // cyan   – EU / global
        default:               return Color(hex: "64748B") // slate  – fallback
        }
    }

    /// SF Symbol for a category, used in rows and chips.
    static func icon(for catClass: String) -> String {
        switch catClass {
        case "cat-approval":   return "checkmark.seal.fill"
        case "cat-regulatory": return "building.columns.fill"
        case "cat-phase3":     return "flask.fill"
        case "cat-biosimilar": return "pills.fill"
        case "cat-crl":        return "xmark.octagon.fill"
        case "cat-deals":      return "arrow.triangle.merge"
        case "cat-outlook":    return "chart.line.uptrend.xyaxis"
        case "cat-eu":         return "globe.europe.africa.fill"
        default:               return "doc.text.fill"
        }
    }
}

extension Color {
    /// Create a Color from a hex string like "1E3A8A" or "#1E3A8A".
    init(hex: String) {
        let s = hex.trimmingCharacters(in: CharacterSet(charactersIn: "#"))
        var rgb: UInt64 = 0
        Scanner(string: s).scanHexInt64(&rgb)
        let r = Double((rgb >> 16) & 0xFF) / 255
        let g = Double((rgb >> 8) & 0xFF) / 255
        let b = Double(rgb & 0xFF) / 255
        self.init(.sRGB, red: r, green: g, blue: b, opacity: 1)
    }
}
