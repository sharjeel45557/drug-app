import SwiftUI

/// Full article view: headline, details, drugs/markets, impact analysis.
struct ArticleDetailView: View {
    let article: Article

    private var color: Color { Theme.color(for: article.catClass) }

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 18) {
                CategoryPill(catClass: article.catClass, label: article.category)

                Text(article.headline)
                    .font(.title2.weight(.bold))
                    .fixedSize(horizontal: false, vertical: true)

                if let d = article.publishedDate {
                    Label(d.formatted(date: .long, time: .omitted), systemImage: "calendar")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }

                Text(article.details)
                    .font(.body)
                    .foregroundStyle(.primary)

                section(title: "Drugs & Markets Affected",
                        icon: "pills.fill",
                        text: article.drugs)

                section(title: "Industry Impact Analysis",
                        icon: "chart.bar.doc.horizontal.fill",
                        text: article.impact)
            }
            .padding()
        }
        .background(Color(.systemGroupedBackground))
        .navigationTitle(article.category)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                ShareLink(item: "\(article.headline)\n\n\(article.impact)") {
                    Image(systemName: "square.and.arrow.up")
                }
            }
        }
    }

    private func section(title: String, icon: String, text: String) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            Label(title, systemImage: icon)
                .font(.subheadline.weight(.semibold))
                .foregroundStyle(color)
            Text(text)
                .font(.callout)
                .foregroundStyle(.primary)
                .fixedSize(horizontal: false, vertical: true)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(14)
        .background(Color(.secondarySystemGroupedBackground))
        .clipShape(RoundedRectangle(cornerRadius: 14, style: .continuous))
    }
}
