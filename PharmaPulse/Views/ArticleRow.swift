import SwiftUI

/// A card in the feed list. Left colour bar encodes the category.
struct ArticleRow: View {
    let article: Article

    private var color: Color { Theme.color(for: article.catClass) }

    var body: some View {
        HStack(spacing: 0) {
            Rectangle()
                .fill(color)
                .frame(width: 5)

            VStack(alignment: .leading, spacing: 8) {
                HStack(spacing: 6) {
                    CategoryPill(catClass: article.catClass, label: article.category)
                    Spacer()
                    if let d = article.publishedDate {
                        Text(d.formatted(.dateTime.month(.abbreviated).day()))
                            .font(.caption2)
                            .foregroundStyle(.secondary)
                    }
                }

                Text(article.headline)
                    .font(.headline)
                    .foregroundStyle(.primary)
                    .multilineTextAlignment(.leading)
                    .fixedSize(horizontal: false, vertical: true)

                Text(article.details)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(3)
                    .multilineTextAlignment(.leading)
            }
            .padding(14)

            Image(systemName: "chevron.right")
                .font(.caption.weight(.semibold))
                .foregroundStyle(.tertiary)
                .padding(.trailing, 12)
        }
        .background(Color(.secondarySystemGroupedBackground))
        .clipShape(RoundedRectangle(cornerRadius: 14, style: .continuous))
        .shadow(color: .black.opacity(0.04), radius: 4, y: 2)
    }
}

/// Small coloured category label.
struct CategoryPill: View {
    let catClass: String
    let label: String

    var body: some View {
        let color = Theme.color(for: catClass)
        Label(label, systemImage: Theme.icon(for: catClass))
            .font(.caption2.weight(.semibold))
            .labelStyle(.titleAndIcon)
            .foregroundStyle(color)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(color.opacity(0.12))
            .clipShape(Capsule())
    }
}
