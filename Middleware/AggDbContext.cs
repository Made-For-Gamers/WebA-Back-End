using Datalayer.Models;
using Microsoft.EntityFrameworkCore;
using Middleware.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Datalayer
{
    public class AggDbContext : DbContext
    {
        public DbSet<User> Users { get; set; }

        public DbSet<Project> Projects { get; set; }

        public DbSet<Category> Categories { get; set; }

        public AggDbContext(DbContextOptions<AggDbContext> options)
       : base(options)
        {
        }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {

            modelBuilder.Entity<Project>()
                .Property("Id");
            modelBuilder.Entity<Project>()
                .Property("UserId");
            modelBuilder.Entity<Project>()
                .Property("CategoryId");
            modelBuilder.Entity<Project>()
                .Property("UserId");

            modelBuilder.Entity<User>()
                .Property("Id");

            modelBuilder.Entity<User>()
                .Property("PasswordHash");

            modelBuilder
              .Entity<Category>()
              .Property(e => e.Engine)
              .HasConversion(
                  v => v.ToString("D"),
                  v => Enum.Parse<GameEngine>(v)
              );

            modelBuilder
              .Entity<Category>()
              .Property(e => e.Platforms)
              .HasConversion(
                  v => string.Join(",", v.Select(e => e.ToString("D")).ToArray()),
                  v => v.Split(new[] { ',' })
                    .Select(e => Enum.Parse(typeof(CompatiblePlatform), e))
                    .Cast<CompatiblePlatform>()
                    .ToList()
              );
            modelBuilder
              .Entity<Category>()
              .Property(e => e.ProgrammingLanguages)
              .HasConversion(
                  v => string.Join(",", v.Select(e => e.ToString("D")).ToArray()),
                  v => v.Split(new[] { ',' })
                    .Select(e => Enum.Parse(typeof(CompatibleLanguages), e))
                    .Cast<CompatibleLanguages>()
                    .ToList()
              );


            //TODO: Move the seeding of the data 
            var cat1 = Guid.NewGuid();
            var cat2 = Guid.NewGuid();
            var cat3 = Guid.NewGuid();

            var userId1 = Guid.NewGuid();

            modelBuilder.Entity<User>().HasData(
                new User() 
                { 
                    Id = 1,
                    UserId = userId1,
                    Email="email@email.email",
                    Name="name",
                    PasswordHash="fakehash"
                });

            modelBuilder.Entity<Category>().HasData(
                new Category()
                {
                    Id = cat1,
                    Engine = GameEngine.Unity,
                    Platforms = new List<CompatiblePlatform>() { CompatiblePlatform.Windows, CompatiblePlatform.Linux },
                    ProgrammingLanguages = new List<CompatibleLanguages>() { CompatibleLanguages.CSharp }
                },
                new Category()
                {
                    Id = cat2,
                    Engine = GameEngine.Unreal,
                    Platforms = new List<CompatiblePlatform>() { CompatiblePlatform.Windows, CompatiblePlatform.Linux, CompatiblePlatform.MacOS },
                    ProgrammingLanguages = new List<CompatibleLanguages>() { CompatibleLanguages.CSharp, CompatibleLanguages.Cpp },
                },
                new Category()
                {
                    Id = cat3,
                    Engine = GameEngine.Random,
                    Platforms = new List<CompatiblePlatform>() { CompatiblePlatform.Android },
                    ProgrammingLanguages = new List<CompatibleLanguages>() { CompatibleLanguages.Js },
                }
            );

            //TODO: Look at the user generation and relationship with the project
            //TODO: Find a better id or filtering key (ex userid)
            modelBuilder.Entity<Project>().HasData(new Project()
            {
                Id = Guid.NewGuid(),
                Name = "Test",
                Description = "Cool test",
                CategoryId = cat1,
                UserId = 1
            },
            new Project()
            {
                Id = Guid.NewGuid(),
                Name = "Test2",
                Description = "Cool test 2",
                CategoryId = cat1,
                UserId = 1
            },
            new Project()
            {
                Id = Guid.NewGuid(),
                Name = "Test3",
                Description = "Cool test 3",
                CategoryId = cat2,
                UserId = 1
            },
            new Project()
            {
                Id = Guid.NewGuid(),
                Name = "Test4",
                Description = "Cool test 4",
                CategoryId = cat3,
                UserId = 1
            });

        }
    }
}
