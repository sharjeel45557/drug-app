import SwiftUI

/// A backward-compatible stand-in for ContentUnavailableView (iOS 17+),
/// so the app also builds and runs on iOS 16.
struct ContentUnavailableCompat: View {
    let title: String
    let systemImage: String
    let description: String

    var body: some View {
        VStack(spacing: 10) {
            Image(systemName: systemImage)
                .font(.largeTitle)
                .foregroundStyle(.secondary)
            Text(title).font(.headline)
            Text(description)
                .font(.subheadline)
                .foregroundStyle(.secondary)
                .multilineTextAlignment(.center)
        }
        .frame(maxWidth: .infinity)
        .padding()
    }
}

struct AboutView: View {
    @Environment(\.dismiss) private var dismiss
    @EnvironmentObject private var store: FeedStore

    var body: some View {
        NavigationStack {
            List {
                Section {
                    VStack(alignment: .leading, spacing: 6) {
                        Text("PharmaPulse")
                            .font(.title2.weight(.bold))
                        Text("Weekly pharma & drug-industry intelligence with impact analysis.")
                            .font(.subheadline)
                            .foregroundStyle(.secondary)
                    }
                    .padding(.vertical, 4)
                }

                Section("This edition") {
                    LabeledContent("Week", value: store.weekRange.isEmpty ? "—" : store.weekRange)
                    LabeledContent("Stories", value: "\(store.articles.count)")
                    if let updated = store.lastUpdated {
                        LabeledContent("Updated", value: updated.formatted(date: .abbreviated, time: .omitted))
                    }
                }

                Section("About the data") {
                    Text("Headlines summarize publicly reported pharma and drug-industry developments. Impact analysis is editorial summary, not investment advice.")
                        .font(.footnote)
                        .foregroundStyle(.secondary)
                }
            }
            .navigationTitle("About")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") { dismiss() }
                }
            }
        }
    }
}
