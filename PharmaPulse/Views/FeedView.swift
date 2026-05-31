import SwiftUI

/// The main news feed: KPI header, category filter, search, and the article list.
struct FeedView: View {
    @EnvironmentObject private var store: FeedStore
    @State private var query = ""
    @State private var selectedCatClass: String? = nil      // nil == "All"
    @State private var showAbout = false

    private var filtered: [Article] {
        store.articles.filter { article in
            let matchesCat = selectedCatClass == nil || article.catClass == selectedCatClass
            let matchesQuery = query.isEmpty
                || article.headline.localizedCaseInsensitiveContains(query)
                || article.drugs.localizedCaseInsensitiveContains(query)
                || article.category.localizedCaseInsensitiveContains(query)
            return matchesCat && matchesQuery
        }
    }

    /// Distinct catClasses present in the current feed, for the filter chips.
    private var availableCats: [String] {
        var seen = Set<String>()
        return store.articles.compactMap { seen.insert($0.catClass).inserted ? $0.catClass : nil }
    }

    var body: some View {
        NavigationStack {
            ScrollView {
                LazyVStack(spacing: 14, pinnedViews: []) {
                    header
                    CategoryChips(cats: availableCats, selected: $selectedCatClass)
                        .padding(.horizontal)

                    if let message = store.errorMessage {
                        banner(message)
                    }

                    ForEach(filtered) { article in
                        NavigationLink(value: article) {
                            ArticleRow(article: article)
                        }
                        .buttonStyle(.plain)
                        .padding(.horizontal)
                    }

                    if filtered.isEmpty {
                        ContentUnavailableCompat(
                            title: "No stories",
                            systemImage: "magnifyingglass",
                            description: "Try a different category or search term."
                        )
                        .padding(.top, 40)
                    }
                }
                .padding(.vertical, 12)
            }
            .background(Color(.systemGroupedBackground))
            .navigationTitle("PharmaPulse")
            .navigationBarTitleDisplayMode(.inline)
            .navigationDestination(for: Article.self) { ArticleDetailView(article: $0) }
            .searchable(text: $query, prompt: "Search drugs, companies, topics")
            .refreshable { await store.refresh() }
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button { showAbout = true } label: { Image(systemName: "info.circle") }
                }
            }
            .sheet(isPresented: $showAbout) { AboutView() }
        }
    }

    // MARK: Header (KPI card)

    private var header: some View {
        VStack(alignment: .leading, spacing: 10) {
            HStack {
                Image(systemName: "waveform.path.ecg")
                Text("Citeline Pharma Intelligence")
                    .font(.subheadline.weight(.semibold))
                Spacer()
            }
            .foregroundStyle(.white.opacity(0.95))

            HStack(alignment: .firstTextBaseline, spacing: 6) {
                Text("\(store.articles.count)")
                    .font(.system(size: 40, weight: .bold, design: .rounded))
                Text("stories this week")
                    .font(.headline.weight(.medium))
                    .foregroundStyle(.white.opacity(0.9))
            }
            .foregroundStyle(.white)

            if !store.weekRange.isEmpty {
                Label(store.weekRange, systemImage: "calendar")
                    .font(.footnote)
                    .foregroundStyle(.white.opacity(0.9))
            }
            if let updated = store.lastUpdated {
                Text("Updated \(updated.formatted(date: .abbreviated, time: .omitted))")
                    .font(.caption2)
                    .foregroundStyle(.white.opacity(0.75))
            }
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(18)
        .background(
            LinearGradient(colors: [Theme.accent, Color(hex: "2563EB")],
                           startPoint: .topLeading, endPoint: .bottomTrailing)
        )
        .clipShape(RoundedRectangle(cornerRadius: 18, style: .continuous))
        .padding(.horizontal)
    }

    private func banner(_ message: String) -> some View {
        Label(message, systemImage: "wifi.exclamationmark")
            .font(.footnote)
            .foregroundStyle(.secondary)
            .frame(maxWidth: .infinity, alignment: .leading)
            .padding(12)
            .background(Color(.secondarySystemBackground))
            .clipShape(RoundedRectangle(cornerRadius: 12, style: .continuous))
            .padding(.horizontal)
    }
}
