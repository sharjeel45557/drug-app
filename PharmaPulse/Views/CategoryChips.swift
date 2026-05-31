import SwiftUI

/// Horizontal, scrollable category filter. The first chip is "All".
struct CategoryChips: View {
    let cats: [String]
    @Binding var selected: String?

    var body: some View {
        ScrollView(.horizontal, showsIndicators: false) {
            HStack(spacing: 8) {
                chip(label: "All", catClass: nil, isOn: selected == nil) { selected = nil }
                ForEach(cats, id: \.self) { cat in
                    chip(label: shortName(cat), catClass: cat, isOn: selected == cat) {
                        selected = (selected == cat) ? nil : cat
                    }
                }
            }
            .padding(.vertical, 2)
        }
    }

    private func chip(label: String, catClass: String?, isOn: Bool, action: @escaping () -> Void) -> some View {
        let color = catClass.map(Theme.color(for:)) ?? Theme.accent
        return Button(action: action) {
            HStack(spacing: 5) {
                if let catClass { Image(systemName: Theme.icon(for: catClass)).font(.caption2) }
                Text(label).font(.caption.weight(.semibold))
            }
            .padding(.horizontal, 12)
            .padding(.vertical, 7)
            .background(isOn ? color : color.opacity(0.12))
            .foregroundStyle(isOn ? Color.white : color)
            .clipShape(Capsule())
        }
        .buttonStyle(.plain)
    }

    /// Map a catClass back to a short human label for the chip.
    private func shortName(_ catClass: String) -> String {
        switch catClass {
        case "cat-approval":   return "Approvals"
        case "cat-regulatory": return "FDA"
        case "cat-phase3":     return "Phase III"
        case "cat-biosimilar": return "Biosimilars"
        case "cat-crl":        return "CRLs"
        case "cat-deals":      return "M&A"
        case "cat-outlook":    return "Outlook"
        case "cat-eu":         return "EU/Global"
        default:               return "Other"
        }
    }
}
